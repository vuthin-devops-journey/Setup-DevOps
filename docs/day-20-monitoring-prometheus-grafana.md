# Day 20: Monitoring — Prometheus + Grafana 📊

**កាលបរិច្ឆេទ:** 15 សីហា 2026
**ប្រធានបទ:** Observability, kube-prometheus-stack, ServiceMonitor,
Application Metrics, Helm repos

---

## 🎯 ហេតុអ្វី Monitoring?

Pipeline ស្វ័យប្រវត្តិរួចហើយ — តែ:

    Push → auto test → auto build → auto deploy ✅
    🙋 តើ app លឿនទេ? RAM ប៉ុន្មាន? Error rate?
       តើដឹងមុន users ត្អូញត្អែរទេ? 😰

**៣ សសរស្តម្ភ Observability:**

| សសរស្តម្ភ | អ្វី | ឧបករណ៍ |
|---|---|---|
| Metrics | លេខតាមពេលវេលា (CPU, requests) | Prometheus |
| Logs | ព្រឹត្តិការណ៍ | Loki / ELK |
| Traces | ដំណើរ request ឆ្លងកាត់ services | Jaeger / Tempo |

ថ្ងៃនេះផ្តោតលើ **Metrics**:

    [App /metrics] ──scrape──▶ [Prometheus] ──query──▶ [Grafana] 📈
    [K8s nodes/pods] ─────────┘

---

## 📍 ឈុតទី ១: បន្ថែម /metrics ចូល Flask

    pip install prometheus-flask-exporter
    metrics = PrometheusMetrics(app)

២ បន្ទាត់ → endpoint /metrics បង្កើតស្វ័យប្រវត្តិ ជាមួយ metrics:
- `flask_http_request_total` — ចំនួន requests តាម method/status
- `flask_http_request_duration_seconds` — latency histogram

**ចំណុចអស្ចារ្យ:** Push code → CI test → build → GHCR → ArgoCD sync
→ pods ថ្មីមាន /metrics — **ដោយមិនប៉ះ cluster ដោយដៃសោះ!**
Pipeline ដែលសាងសង់ពី Day 19 ធ្វើការជំនួសយើង 🤖

---

## 📍 ឈុតទី ២: Helm Repos — Charts សាធារណៈ

    helm repo add prometheus-community https://prometheus-community.github.io/helm-charts
    helm repo update
    helm install monitoring prometheus-community/kube-prometheus-stack -n monitoring

**Helm repo** = ឃ្លាំង charts (ដូច Docker Hub សម្រាប់ images)។

**kube-prometheus-stack** ជា "meta-chart" ដំឡើងទាំងអស់ក្នុងមួយ:
- Prometheus (metrics database + scraper)
- Grafana (visualization)
- Alertmanager (ការជូនដំណឹង)
- node-exporter (metrics ម៉ាស៊ីន)
- kube-state-metrics (metrics K8s objects)
- Prometheus Operator (គ្រប់គ្រងទាំងអស់)
- Dashboards ស្រាប់រាប់សិប!

**មេរៀន:** កុំសាងសង់ពីដំបូងបើមាន chart ស្រាប់ដែលថែទាំដោយ community។

---

## 📍 ឈុតទី ៣: ServiceMonitor — Prometheus ស្គាល់ App យើង

Prometheus Operator ប្រើ CRD (Custom Resource Definition) ដែលហៅថា
ServiceMonitor ដើម្បីដឹងថាត្រូវ scrape អ្វី:

    kind: ServiceMonitor
    metadata:
      labels:
        release: monitoring     ← សំខាន់បំផុត!
    spec:
      selector:
        matchLabels:
          app: myapp            ← រក Service តាម label
      endpoints:
        - port: http            ← ត្រូវការ Service port មានឈ្មោះ!
          path: /metrics

**ចំណុចដែលងាយខុស ២:**
1. `release: monitoring` — Operator រក ServiceMonitors តាម label នេះ
   (ត្រូវនឹងឈ្មោះ Helm release)។ ខុស → Prometheus មិនឃើញ!
2. Service port ត្រូវមាន `name: http` — ServiceMonitor យោងតាមឈ្មោះ

**ធ្វើជា Helm template ជាមួយ `{{- if .Values.metrics.enabled }}`**
→ បិទ/បើកបានតាម environment (dev មិនចាំបាច់ monitoring)។

---

## 📍 ឈុតទី ៤: Grafana Dashboards

Login (admin/admin123) → Dashboards → មានស្រាប់រាប់សិប:

| Dashboard | បង្ហាញអ្វី |
|---|---|
| Kubernetes / Compute Resources / Namespace (Pods) | CPU/RAM របស់ pods ក្នុង namespace |
| Kubernetes / Compute Resources / Cluster | ទិដ្ឋភាពទាំង cluster |
| Node Exporter / Nodes | ធនធានម៉ាស៊ីន |
| Alertmanager / Overview | ស្ថានភាព alerts |

ជ្រើស namespace `default` → ឃើញ myapp និង postgres ជាក្រាហ្វិក 📈

---

## 📍 ឈុតទី ៥: PromQL — ភាសា Query

    flask_http_request_total
      → ចំនួន requests សរុប

    rate(flask_http_request_duration_seconds_count[5m])
      → request rate ក្នុង ៥ នាទីចុងក្រោយ

**Test ជាក់ស្តែង:** refresh /visits ច្រើនដង → query ក្នុង Prometheus
→ ឃើញលេខកើនឡើងផ្ទាល់!

---

## 🧠 Commands ថ្មី

| Command | តួនាទី |
|---|---|
| `helm repo add <name> <url>` | បន្ថែម chart repository |
| `helm repo update` | ធ្វើបច្ចុប្បន្នភាពបញ្ជី charts |
| `kubectl get pods -n monitoring` | មើល pods ក្នុង namespace ជាក់លាក់ |
| `kubectl port-forward svc/x -n ns 3000:80` | tunnel ចូល service ក្នុង namespace |

---

## ⚠️ ចំណាំធនធាន

Monitoring stack ស៊ី RAM ច្រើន (~2GB)។ បើ pods ជាប់ `Pending`:
Docker Desktop → Settings → Resources → Memory ≥ 6GB។

នៅ production stack នេះ run លើ nodes ដាច់ដោយឡែក។

---

## ✅ លទ្ធផល

- Prometheus + Grafana + Alertmanager run ក្នុង cluster
- Dashboards ស្រាប់បង្ហាញ CPU/RAM របស់ myapp និង postgres
- /metrics endpoint ក្នុង Flask (deploy តាម pipeline ស្វ័យប្រវត្តិ!)
- ServiceMonitor → Prometheus scrape app metrics

## 🏆 Project ពេញលេញឥឡូវ

    Build → Test → Package → Publish → Deploy → **Observe** ✅

## 🎯 បន្ទាប់

- Alerting rules (CPU ខ្ពស់ → ជូនដំណឹង)
- Loki (logs aggregation) — សសរស្តម្ភទី ២
- Custom Grafana dashboard សម្រាប់ app metrics
- AWS EKS (cloud ពិត!)
