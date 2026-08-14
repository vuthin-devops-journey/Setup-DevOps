# Day 16: PostgreSQL ក្នុង Cluster + Health Probes ☸️🐘

**កាលបរិច្ឆេទ:** 15 សីហា 2026
**ប្រធានបទ:** Secrets, PVC, Service DNS, Health Probes,
Resource Limits, Rolling Updates

---

## 🎯 គោលដៅ

Full stack ក្នុង Kubernetes — app ២ pods + PostgreSQL + storage
persistent, រួចធ្វើឱ្យវាដល់កម្រិត production-grade។

    ┌────────── Cluster ──────────┐
    │ Service myapp ──▶ app ×2    │
    │                    │ DNS    │
    │ Service postgres ──▶ pg pod │
    │                    │        │
    │                  PVC 1Gi 💾 │
    │ Secret db-secret ──▶ ទាំងពីរ│
    └─────────────────────────────┘

---

## 📍 ឈុតទី ១: Secret — Password ដោយសុវត្ថិភាព

    kubectl create secret generic db-secret \
      --from-literal=POSTGRES_USER=devops ...

**ហេតុអ្វី:** Password មិនគួរសរសេរក្នុង YAML ដែល commit ចូល Git!

**ចំណាំសំខាន់:** K8s Secrets ជា **base64 encoding មិនមែន
encryption**! Production ត្រូវប្រើ Sealed Secrets, External
Secrets Operator, ឬ HashiCorp Vault។

**របៀបប្រើក្នុង YAML:**

| វិធី | ប្រើពេលណា |
|---|---|
| `envFrom: secretRef` | យក keys ទាំងអស់ជា env (postgres) |
| `valueFrom: secretKeyRef` | យក key ជាក់លាក់ (app: DB_USER...) |

---

## 📍 ឈុតទី ២: PVC — Persistent Storage

    kind: PersistentVolumeClaim
    resources: requests: storage: 1Gi

ដូច `volumes: pgdata` ក្នុង docker-compose — ទិន្នន័យរស់នៅ
ទោះ pod ស្លាប់។

**ចំណុចបច្ចេកទេស:** `subPath: pgdata` ចាំបាច់សម្រាប់ Postgres —
បើ mount ត្រង់ទៅ /var/lib/postgresql/data អាច init fail។

**Multi-object YAML:** `---` បំបែក objects ច្រើនក្នុង file តែមួយ
(PVC + Deployment + Service ក្នុង postgres.yaml)។

---

## 📍 ឈុតទី ៣: Service DNS — App ហៅ DB

    env:
      - name: DB_HOST
        value: postgres      ← ឈ្មោះ Service!

K8s DNS ដោះស្រាយ `postgres` → Service IP → pod។
**Concept ដដែលនឹង `DB_HOST: db` ក្នុង docker-compose** —
pods ហៅគ្នាតាមឈ្មោះ មិនមែន IP (ដែលប្តូររហូត)!

**លទ្ធផល:** /visits ដើរក្នុង K8s — count កើនរាល់ refresh 🎉

---

## 📍 ឈុតទី ៤: Persistence Test

    kubectl delete pod -l app=postgres    # លុប db pod!
    → pod ថ្មីកើតវិញ
    → /visits count បន្តពីចាស់ (មិនចាប់ពី 1!) 💾

**SQL ផ្ទាល់ក្នុង pod:**

    kubectl exec -it deployment/postgres -- \
      psql -U devops -d devops -c "SELECT COUNT(*) FROM visits;"

**មេរៀនសំខាន់ — Labels > Names:**
Pod names ជា ephemeral (ប្តូររាល់ពេលកើតឡើងវិញ)។ ប្រើ
`deployment/postgres` ឬ `-l app=postgres` ជំនួស — ដើរជានិច្ច!

---

## 📍 ឈុតទី ៥: Health Probes — Production Grade

**បញ្ហា:** Container run ≠ app ដំណើរការល្អ។ App អាចជាប់,
db ដាច់, ឬមិនទាន់ ready → K8s បញ្ជូន traffic ទៅ pod ខូច!

| Probe | សំណួរ | បើបរាជ័យ |
|---|---|---|
| livenessProbe | នៅរស់ទេ? | Restart container |
| readinessProbe | ត្រៀមទទួល traffic? | ដកចេញពី Service |

**Endpoint /health ដែលសរសេរតាំងពី Day 1 — ឥឡូវទើបប្រើពិត!**

    livenessProbe:
      httpGet: { path: /health, port: 5000 }
      initialDelaySeconds: 10
      periodSeconds: 15

---

## 📍 ឈុតទី ៦: Resources + Rolling Update

**Resources:**

    requests: memory 64Mi, cpu 50m    ← ធានាអប្បបរមា (scheduling)
    limits:   memory 256Mi, cpu 500m  ← ដែនកំណត់ (កុំឱ្យស៊ីអស់)

**Rolling Update — Zero Downtime:**

    strategy:
      rollingUpdate:
        maxSurge: 1          ← បង្កើត pod បន្ថែម ១ បាន
        maxUnavailable: 0    ← មិនអនុញ្ញាតឱ្យខ្វះ pod!

Pod ថ្មីត្រៀម (readiness ✅) សិន ទើបលុប pod ចាស់ →
users មិនដឹងថាមាន deploy!

**Rollout commands:**

| Command | តួនាទី |
|---|---|
| `kubectl rollout status deployment/x` | មើលដំណើរ update |
| `kubectl rollout history deployment/x` | បញ្ជី revisions |
| `kubectl rollout undo deployment/x` | **Rollback ១ command!** |

---

## ✅ លទ្ធផល

- PostgreSQL run ក្នុង cluster ជាមួយ PVC + Secret
- /visits ដើរពេញលេញក្នុង K8s
- Persistence បញ្ជាក់ (delete pod → count បន្ត)
- Probes + resources + rolling update = production-grade!

## 🧠 K8s Objects ដែលស្គាល់ដល់ពេលនេះ

Pod, Deployment, ReplicaSet, Service, Secret, PVC

## 🎯 បន្ទាប់

- ConfigMap (config មិនសម្ងាត់)
- Ingress (ចូលពីខាងក្រៅដោយ domain)
- Helm charts (package ទាំងអស់)
- CI/CD → deploy ចូល K8s ស្វ័យប្រវត្តិ (GitOps!)
