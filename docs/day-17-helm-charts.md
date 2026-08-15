# Day 17: Helm — Package Manager សម្រាប់ Kubernetes ⎈

**កាលបរិច្ឆេទ:** 15 សីហា 2026
**ប្រធានបទ:** Helm Charts, Templates, Values, Releases,
Upgrade/Rollback, Helm Troubleshooting

---

## 🎯 បញ្ហាដែល Helm ដោះស្រាយ

YAML manifests ដើរល្អ — តែ:

| សំណួរ | ជាមួយ YAML ធម្មតា | ជាមួយ Helm |
|---|---|---|
| Deploy ទៅ dev/staging/prod? | copy folder ៣ ដង 😱 | values ផ្សេងគ្នា ✅ |
| Rollback ទាំងកញ្ចប់? | undo ម្តងមួយ object 😰 | `helm rollback` ១ command |
| ដំឡើង Postgres/Redis? | សរសេរ YAML រាប់រយបន្ទាត់ | `helm install` chart ស្រាប់ |

## 🧠 គំនិតស្នូល

| ពាក្យ | ប្រៀបធៀប |
|---|---|
| Chart | Package (ដូច npm/apt package) |
| Values | Config ដែលប្តូរបាន (dev/prod!) |
| Release | Chart ដែល install ក្នុង cluster (មាន version!) |
| Templates | YAML មានកន្លែងទំនេរបំពេញពី values |

    Chart (templates + values) → helm install → Release
                                                (rollback ទាំងកញ្ចប់!)

---

## 📍 ឈុតទី ១: រចនាសម្ព័ន្ធ Chart

    charts/myapp/
    ├── Chart.yaml       ← metadata (name, version)
    ├── values.yaml      ← config center!
    └── templates/
        ├── deployment.yaml
        └── service.yaml

**Go template syntax:**

| Syntax | អត្ថន័យ |
|---|---|
| `{{ .Values.replicaCount }}` | យកតម្លៃពី values.yaml |
| `{{ .Release.Name }}` | ឈ្មោះ release ពេល install |
| `{{ toYaml .Values.resources \| indent 12 }}` | បម្លែង object + indent |

**គោលការណ៍:** អ្វីដែលប្តូរតាម environment → values.yaml។
Template គ្រាន់តែជារូបរាង។

---

## 📍 ឈុតទី ២: Workflow សុវត្ថិភាព

    helm lint charts/myapp        ← ពិនិត្យ syntax
    helm template myapp charts/myapp  ← render មើលមុន install!
    helm install myapp charts/myapp   ← ទើប deploy

**កុំ install ដោយមិន render មើលមុន** — `helm template` បង្ហាញ
YAML ពិតដែលនឹងចូល cluster។

---

## 📍 ឈុតទី ៣: បញ្ហាដែលជួប (Troubleshooting Chain!)

### 1. `helm create charts/myapp` fail
**មូលហេតុ:** parent folder `charts/` មិនមាន
**ដំណោះស្រាយ:** `mkdir -p charts` សិន
**មេរៀន:** tools ខ្លះមិនបង្កើត parent folders (ដូច .github/workflows)

### 2. `ls charts/myapp/` → No such file
**មូលហេតុ:** ឈរនៅក្នុង `templates/` ហើយ relative path ខុស!
**មេរៀន:** ពិនិត្យ `pwd` មុន run commands ដែលមាន relative paths

### 3. `Kubernetes cluster unreachable` (port 50262)
**មូលហេតុ:** Docker Desktop restart → API server port ប្តូរ →
kubeconfig ចាស់ចង្អុលខុស
**ការវិភាគ:** Docker Desktop បង្ហាញ "Running" តែ kubectl fail!
**ដំណោះស្រាយ:** `kubectl config use-context docker-desktop`
ឬ toggle K8s off/on ឱ្យសរសេរ config ថ្មី
**មេរៀន — Config Drift:** cluster ដើរ + kubectl fail = kubeconfig ចាស់!
ពិនិត្យ: `kubectl config view --minify | grep server`

### 4. `cannot re-use a name that is still in use`
តែ `helm list` ទទេ!
**មូលហេតុ:** Orphaned release — install ដំបូងបង្កើត secret +
resources តែ metadata ខូច (kubeconfig ដាច់ពាក់កណ្តាល)
**ការស៊ើបអង្កេត:**

    kubectl get secrets -A | grep helm    ← releases ពិត!
    kubectl get all                        ← resources ពិត

រកឃើញ: `sh.helm.release.v1.myapp.v1` + deployment/service myapp
**ដំណោះស្រាយ:** លុបទាំង secret + resources ឬប្រើឈ្មោះ release ថ្មី

**មេរៀនធំ:** Helm រក្សា metadata ជា **Secrets ក្នុង cluster**
(`sh.helm.release.v1.<name>.<rev>`)។ ពេល `helm list` មិនត្រូវនឹង
ការពិត — មើល secrets ដោយផ្ទាល់!

---

## 📍 ឈុតទី ៤: Helm Magic — Upgrade & Rollback

    helm upgrade flaskapp charts/myapp --set replicaCount=4
    → 4 pods (មិនបាច់កែ file — --set override!)

    helm history flaskapp        → បញ្ជី revisions
    helm rollback flaskapp 1     → ត្រឡប់ 2 pods ក្នុង ១ command!

**Rollback ទាំងកញ្ចប់** — deployment + service + config ទាំងអស់
ត្រឡប់ជាមួយគ្នា។ នេះជាអ្វីដែល kubectl ធ្វើមិនបានងាយ!

---

## 🧠 Helm Commands

| Command | តួនាទី |
|---|---|
| `helm lint <chart>` | ពិនិត្យ syntax |
| `helm template <rel> <chart>` | Render មើលមុន install |
| `helm install <rel> <chart>` | Install ថ្មី |
| `helm upgrade <rel> <chart>` | Update |
| `helm upgrade --install` | ធ្វើទាំងពីរ — **ប្រើក្នុង CI/CD!** |
| `helm list -A --all` | Releases ទាំងអស់គ្រប់ namespace |
| `helm history <rel>` | ប្រវត្តិ revisions |
| `helm rollback <rel> <rev>` | ត្រឡប់ក្រោយ |
| `helm uninstall <rel>` | លុបទាំងកញ្ចប់ |

---

## ✅ លទ្ធផល

- Helm chart ពេញលេញក្នុង repo (charts/myapp/)
- Release deployed + upgrade + rollback ដំណើរការ
- Troubleshooting: config drift, orphaned releases
- Chart ជា IaC កម្រិតខ្ពស់ — parameterized, versioned, rollback-able

## 🎯 បន្ទាប់

- CI/CD → helm upgrade --install ស្វ័យប្រវត្តិ (GitOps!)
- ឬ Ingress (domain access)
- ឬ ចាកចេញទៅ Cloud (AWS EKS)
