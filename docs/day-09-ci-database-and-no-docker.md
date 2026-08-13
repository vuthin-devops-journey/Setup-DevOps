# Day 9: CI ជាមួយ Database + ធ្វើការនៅម៉ាស៊ីនគ្មាន Docker

**កាលបរិច្ឆេទ:** 14 សីហា 2026
**ប្រធានបទ:** Service Containers ក្នុង CI, pytest -k, CI ជា source of truth

---

## 🎯 គោលដៅ

- Test /visits endpoint ជាមួយ PostgreSQL ពិតក្នុង GitHub Actions
- រៀនធ្វើការនៅម៉ាស៊ីនដែលគ្មាន Docker (ការិយាល័យ)
- យល់ថា CI ជា source of truth ពេល environments ខុសគ្នា

---

## 📍 ឈុតទី ១: Service Containers ក្នុង ci.yml

GitHub Actions អាច run Postgres ក្បែរ runner — ដូច docker-compose
តែក្នុង cloud:

    services:
      postgres:
        image: postgres:16-alpine
        env: ...
        ports:
          - 5432:5432
        options: --health-cmd "pg_isready -U devops" ...

Concepts ពី compose (services, healthcheck, env) — ដដែលទាំងអស់
គ្រាន់តែ syntax ខុសបន្តិច!

---

## 📍 ឈុតទី ២: បញ្ហាជាបន្តបន្ទាប់ (Debugging Marathon!)

### បញ្ហា ១: ModuleNotFoundError: psycopg2
**មូលហេតុ:** requirements.txt កែហើយ តែភ្លេច pip install
**មេរៀន:** requirements.txt ជាបញ្ជី — ត្រូវ install ទើបចូល venv!

### បញ្ហា ២: SyntaxError: invalid character '←'
**មូលហេតុ:** Copy ចំណាំពន្យល់ (← បន្ទាត់ទទេ ២!) ចូល code ផង
**មេរៀន:** អាន error ចុងក្រោយ — វាប្រាប់ file + line + តួអក្សរច្បាស់!

### បញ្ហា ៣: collected 6 items (គួរ 8)
**មូលហេតុ:** Paste មិនដល់ចុង — tests /visits បាត់
**មេរៀន:** អាន "collected N items" ជានិច្ច — pytest ប្រាប់ថា
រកឃើញប៉ុន្មាន!

### បញ្ហា ៤: password authentication failed (ម៉ាស៊ីនផ្ទះ)
**ការវិភាគ:** Connection ទៅដល់ server តែ auth fail —
ទំនងជា Windows Postgres ស្រាប់ជាន់ port 5432 ឬ volume ចាស់
**ស្ថានភាព:** មិនទាន់ដោះស្រាយ — CI នឹងបញ្ជាក់ថា code ល្អ

### បញ្ហា ៥: Docker មិនអាចប្រើនៅការិយាល័យ
**ដំណោះស្រាយ:** pytest -k "not visits" → 6 passed local
CI test ទាំង 8 ជាមួយ Postgres ជំនួស!

---

## 📍 ឈុតទី ៣: CI ជា Source of Truth

    ការិយាល័យ (no Docker)  → 6 tests ✅
    GitHub CI (Postgres)    → 8 tests ✅ ← ការសម្រេចចុងក្រោយ!
    ផ្ទះ (port conflict)    → environment issue មិនមែន code issue

**មេរៀនធំបំផុត:** ពេល environments ខុសគ្នា (ផ្ទះ/ការិយាល័យ/CI) —
CI ជាកន្លែងវិនិច្ឆ័យ។ CI បៃតង = code ត្រឹមត្រូវ ទោះ local fail
ដោយសារ environment ក៏ដោយ។

---

## 🧠 ជំនាញថ្មី

| ជំនាញ | ពិពណ៌នា |
|---|---|
| `pytest -k "not visits"` | Run tests ដោយច្រោះតាមឈ្មោះ |
| `cat >> file << 'EOF'` | Append អត្ថបទចូល file តាម bash |
| `DB_PORT=5433 pytest` | កំណត់ env var សម្រាប់ command មួយ |
| Service containers | Database ក្នុង CI runner |
| Run one-check one | ពិនិត្យលទ្ធផលម្តងមួយ កុំ paste ជាប់គ្នាទាំង fail |

## ✅ លទ្ធផល

- CI test ទាំង 8 ជាមួយ Postgres ពិតក្នុង cloud
- ចេះធ្វើការគ្រប់ environment: មាន/គ្មាន Docker
- Debugging skills កាន់តែខ្លាំង — ៥ បញ្ហាក្នុងមួយថ្ងៃ! 💪

## 🎯 បន្ទាប់

Push Docker image ទៅ GitHub Container Registry (CD ជំហានទី១!)
