# Day 15: YAML Manifests — Infrastructure as Code! ☸️📄

**កាលបរិច្ឆេទ:** 14 សីហា 2026
**ប្រធានបទ:** Declarative K8s, Deployment/Service YAML, Labels &
Selectors, kubectl apply, Idempotency

---

## 🎯 ការផ្លាស់ប្តូរគំនិត

    Imperative (commands):  "ធ្វើអ្វី" — kubectl create/scale/delete
    Declarative (YAML):     "ចង់បានអ្វី" — kubectl apply -f

| Commands | YAML Manifests |
|---|---|
| ចងចាំក្នុងក្បាល | File ក្នុង Git ✅ |
| ម៉ាស៊ីនថ្មី = វាយម្តងទៀត | apply -f ដូចគ្នាគ្រប់កន្លែង |
| Review មិនបាន | PR review បាន! |
| ប្រវត្តិបាត់ | git log = ប្រវត្តិពេញ |
| create → error បើមាន | apply → idempotent |

**នេះជាមូលដ្ឋាន GitOps** — cluster ទាំងមូលពិពណ៌នាក្នុង Git។

---

## 📍 ឈុតទី ១: deployment.yaml

**រចនាសម្ព័ន្ធ (pattern ដដែលគ្រប់ K8s object):**

| ផ្នែក | អត្ថន័យ |
|---|---|
| apiVersion + kind | ប្រភេទ object (apps/v1, Deployment) |
| metadata.name/labels | អត្តសញ្ញាណ |
| spec.replicas: 2 | Desired state — ២ pods ជានិច្ច |
| spec.selector.matchLabels | Deployment រក pods តាម label |
| spec.template | ពុម្ព pod (image, ports, labels) |

**គំនិតស្នូល — Labels ភ្ជាប់អ្វីៗគ្នា:**
Deployment រក pods តាម label → Service ក៏រក pods តាម label ដដែល។
Labels ជា "កាវ" ភ្ជាប់ K8s objects!

---

## 📍 ឈុតទី ២: service.yaml — Networking

**បញ្ហា:** Pods កើត/ស្លាប់ → IP ប្តូររហូត។ Traffic ទៅរកយ៉ាងម៉េច?

**ចម្លើយ: Service** = អាសយដ្ឋានថេរ + load balancer

    Service "myapp" (ClusterIP ថេរ, port 80)
        │ selector: app=myapp
        ├──▶ pod-1 :5000
        └──▶ pod-2 :5000   ← ចែក traffic ស្វ័យប្រវត្តិ

`port: 80` = port របស់ Service | `targetPort: 5000` = port ក្នុង pod

ចាំ `DB_HOST: db` ក្នុង docker-compose? Service = concept ដដែល —
pods ហៅគ្នាតាមឈ្មោះ មិនមែន IP!

---

## 📍 ឈុតទី ៣: kubectl apply — Idempotency

    kubectl apply -f k8s/     ← ទាំង folder ក្នុងមួយ command!

**លទ្ធផលតាមស្ថានភាព:**

| ស្ថានភាព | Output |
|---|---|
| Object ថ្មី | created |
| មានស្រាប់ + ខុសពី file | configured ← កែតាមភាពខុសគ្នា |
| មានស្រាប់ + ដូច file | unchanged ← មិនធ្វើអ្វី |

**Idempotency:** run ១ ដង ឬ ១០០ ដង លទ្ធផលដូចគ្នា —
CI/CD pipelines ពឹងលើគុណសម្បត្តិនេះ!

---

## 📍 ឈុតទី ៤: Declarative Power Tests

**Test 1 — លុប pods ទាំងអស់:**

    kubectl delete pod --all
    kubectl get pods    → ២ ថ្មីកើតវិញភ្លាម! (desired state = 2)

**Test 2 — កែ YAML → cluster ប្រែ:**

    sed -i 's/replicas: 2/replicas: 4/' k8s/deployment.yaml
    kubectl apply -f k8s/    → configured
    kubectl get pods         → 4 pods!

**នេះជា IaC ពិត:** ប្តូរ file → apply → ហេដ្ឋារចនាសម្ព័ន្ធប្រែតាម។
File ជាការពិត cluster ដើរតាម។

---

## 📍 ឈុតទី ៥: រកឃើញ — ReplicaSet Hash ប្តូរ

Pods ពី YAML: `myapp-5b5f98c966-xxxxx`
Pods ពី command មុន: `myapp-7456f95bc6-xxxxx`

**មូលហេតុ:** YAML បន្ថែម `labels: app: myapp` ចូល pod template
→ template ខុស → hash ថ្មី → ReplicaSet ថ្មី។

K8s គណនា hash ពី template — ការប្តូរតូចបំផុតក៏បង្កើត
ReplicaSet ថ្មី (មូលដ្ឋានរបស់ rolling updates!)។

---

## 🧠 Commands ថ្មី

| Command | តួនាទី |
|---|---|
| `kubectl apply -f <file/folder>` | បង្កើត/កែតាម manifest |
| `kubectl get services` | មើល services |
| `kubectl port-forward service/x 5000:80` | tunnel តាម Service |
| `kubectl delete pod --all` | លុប pods ទាំងអស់ (test!) |
| `kubectl get all` | resources ទាំងអស់ក្នុងមួយសម្លឹង |

---

## ✅ លទ្ធផល

- k8s/deployment.yaml + service.yaml ចូល Git = IaC!
- 2 pods តាម desired state
- Service ចែក traffic ទៅ pods
- បញ្ជាក់ declarative: delete --all → កើតវិញ, កែ replicas → apply → ប្រែ

## 🎯 បន្ទាប់

PostgreSQL ចូល cluster:
- Secret (password) + ConfigMap (config)
- StatefulSet ឬ Deployment + PVC សម្រាប់ db
- /visits ដើរក្នុង K8s!
