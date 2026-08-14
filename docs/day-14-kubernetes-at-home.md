# Day 14: Kubernetes នៅម៉ាស៊ីនផ្ទះ — Cluster ទី ២! ☸️🏠

**កាលបរិច្ឆេទ:** 14 សីហា 2026
**ប្រធានបទ:** kubeconfig, contexts, minikube on Windows,
terminal discipline, K8s object lifecycle

---

## 🎯 គោលបំណង

ធ្វើមេរៀន Day 13 ម្តងទៀតនៅម៉ាស៊ីនផ្ទះ — ដើម្បីបញ្ជាក់ថា
kubectl commands ដូចគ្នា ១០០% គ្រប់ cluster ហើយចំណេះដឹង
មិនជាប់នឹងបរិស្ថានណាមួយ។

---

## 📍 ឈុតទី ១: kubeconfig គ្មាន — Cluster មិនទាន់មាន

**បញ្ហា:**

    kubectl get nodes
    → dial tcp [::1]:8080: connection refused
    → error: current-context is not set

**ការវិភាគ:**

    kubectl config get-contexts  → ទទេ
    ls ~/.kube/config            → No such file!

**មេរៀនសំខាន់:** error port 8080 ក្នុង kubectl មិនមែន network
issue ទេ — វាជា **fallback default** ពេល kubeconfig គ្មាន!
File ~/.kube/config កើតដោយស្វ័យប្រវត្តិពេល cluster start ជោគជ័យ។

**Debugging ladder ត្រឹមត្រូវ:**
1. kubectl error → 2. context មានទេ? → 3. ~/.kube/config មានទេ?
→ 4. cluster ដែល create វាដំណើរការទេ?

---

## 📍 ឈុតទី ២: ជម្រើស Cluster នៅ Windows

| ជម្រើស | លក្ខខណ្ឌ |
|---|---|
| Docker Desktop K8s | Settings → Kubernetes → Enable (GUI!) |
| minikube --driver=docker | ត្រូវការតែ Docker engine |

**មេរៀន:** ជំហានខ្លះជា GUI (Docker Desktop settings) — terminal
ជួយមិនបាន។ `kubectl config use-context docker-desktop` នឹង fail
រហូតដល់ cluster ត្រូវបាន enable ក្នុង app។

**ជម្រើសដែលយក:** minikube — ស្គាល់ស្រាប់ពី Codespace,
commands ដូចគ្នា, ត្រូវការតែ Docker engine។

---

## 📍 ឈុតទី ៣: Terminal Discipline (មេរៀនអនុវត្តន៍!)

**បញ្ហា:** Paste commands ១០ បន្ទាត់ជាមួយគ្នា →
`kubectl get pods -w` (watch) ជាប់រង់ចាំ → commands ក្រោយៗ
តម្រង់ជួរ → run ព្រាវៗពេល Ctrl+C → ស្ថានភាពច្របូកច្របល់
(pod ឯកឯង + deployment pod លាយគ្នា)

**ច្បាប់:**

    ❌ Paste ១០ បន្ទាត់ → មិនដឹងអ្វីកើតឡើង
    ✅ ១ command → Enter → អាន → យល់ → បន្ត

ជាពិសេស interactive commands ដែលមិន return prompt:
`kubectl get pods -w`, `kubectl port-forward`, `minikube start`,
`docker compose up` (foreground)

---

## 📍 ឈុតទី ៤: create vs apply

**បញ្ហា:** `error: deployments.apps "myapp" already exists`

| Command | អាកប្បកិរិយា |
|---|---|
| `kubectl create` | បង្កើតថ្មី — error បើមានហើយ |
| `kubectl apply -f` | ធានាឱ្យត្រូវតាម file — មាន/គ្មាន ក៏ដើរ ✅ |
| `kubectl replace` | ជំនួសទាំងស្រុង |

**apply = ជម្រើស GitOps** — idempotent (run ម្តង ឬ ១០០ ដង
លទ្ធផលដូចគ្នា)។ នេះជាមូលហេតុ production ប្រើ YAML + apply។

**សម្អាត:**

    kubectl delete deployment myapp
    kubectl get all        ← មើល resources ទាំងអស់ក្នុងមួយសម្លឹង

---

## 📍 ឈុតទី ៥: រកឃើញគួរឱ្យចាប់អារម្មណ៍ — ReplicaSet Hash

Pod នៅផ្ទះឈ្មោះ `myapp-7456f95bc6-2kfrb` —
hash `7456f95bc6` **ដូចនឹង Codespace**!

**មូលហេតុ:** K8s គណនា hash ពី **pod template**
(image, ports, labels)។ Template ដូចគ្នា → hash ដូចគ្នា
ទោះ cluster ផ្សេងគ្នា — declarative determinism!

---

## ✅ លទ្ធផល

- Cluster ទី ២ ដំណើរការនៅម៉ាស៊ីនផ្ទះ
- Pod ពី GHCR image Running
- port-forward → **localhost:5000 ដើរផ្ទាល់ក្នុង Chrome**
  (មិនបាច់ tunnel ដូច Codespace — cluster នៅក្នុងម៉ាស៊ីនផ្ទាល់!)
- Self-healing + scaling ហាត់ម្តងទៀត

## 🧠 Environment Map ចុងក្រោយ

| កន្លែង | Cluster | ចូល app |
|---|---|---|
| Codespace ☁️ | minikube in Docker | GitHub tunnel URL |
| ផ្ទះ 🏠 | minikube / Docker Desktop | localhost:5000 ផ្ទាល់ |
| CI 🤖 | (មិនទាន់) | — |

## 🎯 បន្ទាប់ — មេរៀនទី ២: YAML Manifests

k8s/deployment.yaml + service.yaml → kubectl apply -f k8s/
→ commit Git = Infrastructure as Code → ផ្លូវទៅ GitOps!
