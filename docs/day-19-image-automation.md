# Day 19: Image Automation — Pipeline ស្វ័យប្រវត្តិ ១០០%! 🤖

**កាលបរិច្ឆេទ:** 15 សីហា 2026
**ប្រធានបទ:** CI writes / CD reads, GITHUB_SHA tagging, [skip ci]

---

## 🎯 បញ្ហាចុងក្រោយដែលនៅសល់

    CI build image:latest → GHCR ✅
    ArgoCD មើល values.yaml → tag: latest (មិនប្តូរ!)
    → Git មិនប្តូរ → ArgoCD មិន sync → pods នៅប្រើ image ចាស់ 😱

**ដំណោះស្រាយ — "CI writes, CD reads":**

    CI: build image:<SHA> → push GHCR
      → sed values.yaml (tag: <SHA>) → git commit
          ↓ Git ប្តូរ!
    ArgoCD: sync → rolling update → pods ថ្មី 🎉

---

## 📍 ឈុតទី ១: Job update-manifest

    update-manifest:
      needs: build-and-push
      permissions:
        contents: write        ← CI សរសេរចូល repo!
      steps:
        - sed -i "s|tag: .*|tag: ${GITHUB_SHA}|" charts/myapp/values.yaml
        - git commit -m "ci: update image tag [skip ci]"
        - git push

**ចំណុចសំខាន់បំផុត — [skip ci]:**
បើគ្មាន: CI commit → trigger CI → commit → trigger... រង្វិលអស់កល្ប! 🔁
`[skip ci]` ក្នុង commit message ប្រាប់ GitHub Actions កុំ run។

**`git diff --staged --quiet ||`** = commit តែពេលមានការប្តូរពិត។

---

## 📍 ឈុតទី ២: ហេតុអ្វី SHA ជាជាង latest?

| Tag | បញ្ហា/គុណសម្បត្តិ |
|---|---|
| `latest` | មិនដឹងថា image ណា! rollback មិនបាន, Git មិនប្តូរ |
| `<commit-SHA>` | Traceable ១០០% — image ណាមកពី commit ណា ✅ |

**Immutable tags** = ស្តង់ដារ production។ Rollback = ប្តូរ tag
ក្នុង Git ត្រឡប់ក្រោយ → ArgoCD deploy version ចាស់!

---

## 📍 ឈុតទី ៣: End-to-End Test

**អ្វីដែលធ្វើ:** កែ version 1.0.0 → 2.0.0 ក្នុង app.py + test_app.py

**អ្វីដែលកើតឡើងស្វ័យប្រវត្តិ:**

    1. git push (អ្នកធ្វើតែប៉ុណ្ណេះ!)
    2. CI: flake8 + 8 tests ជាមួយ PostgreSQL ✅
    3. CI: docker build → GHCR (tag = SHA)
    4. CI: sed values.yaml → commit [skip ci]
    5. ArgoCD: sync
    6. K8s: rolling update (zero downtime)
    7. Browser /version → {"version": "2.0.0"} 🎯

**គ្មាន kubectl apply។ គ្មាន helm upgrade។ គ្មាន docker push ដោយដៃ។**

---

## 🏆 ខ្សែសង្វាក់ពេញលេញ

    Developer → git push
        ↓
    [CI] lint → test (with DB) → build → push GHCR → update manifest
        ↓
    [Git] source of truth (code + config + image tag)
        ↓
    [CD] ArgoCD pull → sync → K8s rolling update
        ↓
    [Production] pods ថ្មី, zero downtime, self-healing

## 🧠 គោលការណ៍សំខាន់

1. **Separation of concerns:** CI build/test, CD deploy — ដាច់ពីគ្នា
2. **Git as source of truth:** អ្វីៗទាំងអស់ (code, config, tags) ក្នុង Git
3. **Immutable artifacts:** image tag = SHA មិនប្តូរ
4. **Pull-based CD:** cluster មិនបើកចេញក្រៅ (សុវត្ថិភាព)
5. **Audit trail:** git log = ប្រវត្តិ deploy ទាំងអស់!

## ⚠️ ចំណាំអនុវត្តន៍

venv activate ភ្លេចញឹកញាប់ → `flake8: command not found`។
ដំណោះស្រាយ: alias `devops` = cd + activate ក្នុងមួយ command។

## 🎯 បន្ទាប់

- Ingress (domain access)
- Monitoring (Prometheus + Grafana)
- AWS EKS (cloud ពិត)
- Multi-environment (dev/staging/prod values)
