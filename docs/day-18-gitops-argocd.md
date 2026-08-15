# Day 18: GitOps ជាមួយ ArgoCD — បញ្ចប់ខ្សែសង្វាក់! 🔄

**កាលបរិច្ឆេទ:** 15 សីហា 2026
**ប្រធានបទ:** GitOps, ArgoCD, Namespaces, Self-Heal, Auto-Sync

---

## 🎯 បញ្ហាដែល GitOps ដោះស្រាយ

មុនពេលនេះ:

    Push → CI test ✅ → build image ✅ → GHCR ✅
                                          ↓
                          🙋 អ្នក run helm upgrade ដោយដៃ!

**គំរូ CD ២ ប្រភេទ:**

| គំរូ | របៀប | ការវាយតម្លៃ |
|---|---|---|
| Push-based | CI មាន cluster credentials → deploy | CI ត្រូវការសិទ្ធិចូល cluster (ហានិភ័យ) |
| Pull-based (GitOps) | Agent ក្នុង cluster មើល Git → sync ខ្លួនឯង | Cluster មិនបើកចេញក្រៅ ✅ |

**ArgoCD = pull-based:**

    Git repo (source of truth)
        ↑ commit              ↓ ArgoCD មើលរាល់ ៣ នាទី
    អ្នក ──────────▶ [ArgoCD ក្នុង cluster] → sync → resources ប្រែ!

---

## 📍 ឈុតទី ១: ដំឡើង ArgoCD

    kubectl create namespace argocd
    kubectl apply -n argocd -f https://raw.githubusercontent.com/\
      argoproj/argo-cd/stable/manifests/install.yaml

**Namespace ថ្មី:** ការបែងចែក resources ក្នុង cluster (ដូច folders)។
ArgoCD រស់នៅ `argocd` ដាច់ពី app យើង (`default`)។

**ចូល UI:**

    Terminal 2: kubectl port-forward svc/argocd-server -n argocd 8080:443
    Password:   kubectl -n argocd get secret argocd-initial-admin-secret \
                  -o jsonpath="{.data.password}" | base64 -d
    Browser:    https://localhost:8080 (admin / password)

**មេរៀន:** port-forward ត្រូវ run ជាប់ក្នុង terminal ដាច់ដោយឡែក —
បិទ = UI ដាច់ (ERR_CONNECTION_REFUSED)។ DevOps engineers តែងបើក
terminals ២-៣ ព្រមគ្នា។

---

## 📍 ឈុតទី ២: Application Manifest — បេះដូង GitOps

    kind: Application
    spec:
      source:
        repoURL: https://github.com/.../Setup-DevOps.git
        path: charts/myapp          ← Helm chart ក្នុង Git!
        targetRevision: main
      syncPolicy:
        automated:
          prune: true       ← លុប resources ដែលដកចេញពី Git
          selfHeal: true    ← កែពេលមាននរណាប្តូរដោយដៃ!

**ចំណុចសំខាន់:** ArgoCD អាន **ពី Git** មិនមែនពី disk local —
ដូច្នេះ chart ត្រូវ push ទៅ GitHub មុន!

---

## 📍 ឈុតទី ៣: លទ្ធផល — Synced & Healthy

ArgoCD UI បង្ហាញ:

    myapp
    Status:      💚 Healthy  ✅ Synced
    Repository:  github.com/vuthin-devops-journey/Setup-DevOps.git
    Path:        charts/myapp
    Namespace:   default

UI មាន application graph: Application → Deployment → ReplicaSet →
Pods + Service។ ចុចលើ pod → logs, events, manifest ក្នុង browser!

---

## 📍 ឈុតទី ៤: Demo ១ — Git Commit = Deployment

    sed -i 's/replicaCount: 2/replicaCount: 4/' charts/myapp/values.yaml
    git commit -am "chore: scale to 4" && git push
    → ArgoCD sync → kubectl get pods → 4 pods!

**គ្មាន kubectl apply, គ្មាន helm upgrade** — commit ប៉ុណ្ណោះ!

---

## 📍 ឈុតទី ៥: Demo ២ — Self-Heal

    kubectl scale deployment myapp --replicas=1    ← ប្តូរដោយដៃ
    → រង់ចាំបន្តិច → kubectl get pods → ត្រឡប់ចំនួនក្នុង Git!

**ArgoCD ឃើញ cluster ≠ Git → កែឯង។ Git ឈ្នះជានិច្ច។**

**អត្ថប្រយោជន៍:** គ្មាន "config drift" — អ្វីដែលនៅ Git = អ្វីដែល
run ក្នុង production ជានិច្ច។ ការផ្លាស់ប្តូរទាំងអស់មាន audit trail
(git log) និង review (PR)។

---

## 🧠 គោលការណ៍ GitOps ៤

1. **Declarative** — ប្រព័ន្ធទាំងមូលពិពណ៌នាជា code
2. **Versioned** — Git ជា source of truth (មាន history!)
3. **Pulled automatically** — agents ទាញពី Git
4. **Continuously reconciled** — កែភាពខុសគ្នាឥតឈប់

---

## ⚠️ ចំណាំសុវត្ថិភាព (មេរៀនផ្ទាល់ខ្លួន!)

កុំ paste passwords/tokens/secrets ចូល chat, ticket, ឬ PR។
ប្រើ placeholder ជំនួស។ បើលេចធ្លាយ — ប្តូរភ្លាម។
DevOps ធ្វើការជាមួយ credentials ច្រើន — ទម្លាប់នេះសំខាន់!

---

## ✅ លទ្ធផល

- ArgoCD run ក្នុង cluster + UI
- Application synced ពី Git (Helm chart)
- Auto-sync: push → deploy ស្វ័យប្រវត្តិ
- Self-heal: manual change → ArgoCD កែត្រឡប់

## 🏆 ខ្សែសង្វាក់ពេញលេញ

    Code → Git → CI (test+lint) → Docker build → GHCR
                                                  ↓
                ArgoCD មើល Git ──▶ sync ──▶ Kubernetes

## 🎯 បន្ទាប់

- Ingress (domain access)
- Image tag automation (CI update values.yaml → auto deploy!)
- AWS EKS (cloud ពិត)
- Monitoring (Prometheus + Grafana)
