# Day 10: Publish Docker Image ទៅ GHCR — CD ជំហានទី១! 📦

**កាលបរិច្ឆេទ:** 14 សីហា 2026

## 🎯 អ្វីដែលសម្រេចបាន

Pipeline ពេញលេញ: test ✅ (25s) → build-and-push ✅ (31s)
Image publish ទៅ ghcr.io — ម៉ាស៊ីនណាក៏ pull បាន!

## 💡 Concepts ថ្មី

| Concept | អត្ថន័យ |
|---|---|
| `needs: test` | Job dependency — build រង់ចាំ test ✅ |
| `if: github.ref == main` | Build តែលើ main — PR គ្រាន់តែ test |
| `secrets.GITHUB_TOKEN` | Token ស្វ័យប្រវត្តិ — គ្មាន password manual |
| `permissions: packages: write` | អនុញ្ញាត push ទៅ GHCR |
| Tags: latest + SHA | Traceable — ដឹង image មកពី commit ណា |

## 🔑 ចំណុចសំខាន់

GitHub ជាអ្នក build — ម៉ាស៊ីនការិយាល័យគ្មាន Docker ក៏បង្កើត
image បាន! CI/CD = ការងារធ្ងន់នៅ cloud។

## 🎯 បន្ទាប់

Pull image ពី GHCR នៅម៉ាស៊ីនផ្ទះ + ដោះស្រាយ port 5432 conflict
រួចឆ្ពោះទៅ Kubernetes! ☸️
