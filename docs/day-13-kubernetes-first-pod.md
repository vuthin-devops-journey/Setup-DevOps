# Day 13: Kubernetes — Pod ដំបូង + Self-Healing! ☸️

**កាលបរិច្ឆេទ:** 14 សីហា 2026

## 🎯 អ្វីដែលសម្រេចបាន

- minikube cluster ក្នុង Codespace (K8s នៅការិយាល័យ!)
- Pod ដំបូងពី GHCR image → Running
- Debug ImagePullBackOff ពេញមួយវដ្ត
- Self-healing + scaling ដោយ Deployment

## 📍 ImagePullBackOff Debugging Journey

1. kubectl logs → "failing to pull image"
2. kubectl describe pod → Events → "unauthorized"!
3. រកឃើញ: repo public ≠ package public (២ settings ផ្សេង!)
4. Package visibility → Public ត្រូវ disable ដោយ org policy
5. ដំណោះស្រាយ: org settings → allow public packages
   → package public → pod Running 12s!

**មេរៀន:** describe pod → Events = ជំហានទី១ រាល់ pod issues!
Backoff pattern (x4 pulls, x9 backoffs) = exponential retry។

## 📍 Concepts

| K8s | ស្គាល់ពី |
|---|---|
| Pod | ≈ docker run (ឯកតាតូចបំផុត) |
| kubectl run/logs/delete | ≈ docker commands |
| port-forward | ≈ Codespace tunnel / -p flag |
| Deployment | ថ្មី! អ្នកមើលថែ pods |

## 📍 Self-Healing Demo

- Pod ឯកឯង delete → បាត់រហូត (គ្មានអ្នកការពារ)
- Deployment pod delete → កើតវិញក្នុងវិនាទី! 🤯
- kubectl scale --replicas=3 → 3 pods ភ្លាម

**នេះជាមូលហេតុ production ប្រើ K8s!**

## 🎯 បន្ទាប់

YAML manifests (IaC!), Services, ភ្ជាប់ database ចូល cluster