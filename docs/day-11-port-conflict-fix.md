# Day 11: ដោះស្រាយ Port Conflict + Location-Aware Workflow

**កាលបរិច្ឆេទ:** 14 សីហា 2026
**ប្រធានទប:** Port conflicts, netstat/tasklist, DB_PORT env var,
ធ្វើការតាមទីកន្លែង (ការិយាល័យ/ផ្ទះ/CI)

---

## 📍 ឈុតទី ១: ស៊ើបអង្កេត password authentication failed

**បញ្ហា (ម៉ាស៊ីនផ្ទះ):** pytest ភ្ជាប់ db បាន តែ auth fail

**ការស៊ើបអង្កេត:**

    netstat -ano | grep 5432     → PID 4892 កាន់ port
    tasklist | grep 4892         → postgres.exe (Windows Service!)

**រកឃើញ:** Windows PostgreSQL ដំឡើងស្រាប់កាន់ 5432 —
pytest ភ្ជាប់ទៅវា (មិនមែន Docker db) → user devops គ្មាន → fail!

**មេរៀន:** "password failed" មិនមែនតែងតែ password ខុសទេ —
អាចជាភ្ជាប់ទៅ server ខុស! netstat + tasklist = ឧបករណ៍រកពិរុទ្ធជន។

---

## 📍 ឈុតទី ២: ដំណោះស្រាយ — DB_PORT Environment Variable

**ជម្រើស:** បិទ Windows postgres? ទេ — មិនដឹងកម្មវិធីអ្វីប្រើ។
**ជម្រើសល្អ:** ប្តូរ Docker ទៅ port 5433 — មិនប៉ះអ្វីដែលមានស្រាប់!

**ការកែ ៣ កន្លែង:**
1. compose db: "5433:5432" (host 5433 → container 5432)
2. compose web: DB_PORT: "5432" (ក្នុង network នៅ 5432 ដដែល!)
3. app.py: DB_PORT = os.environ.get("DB_PORT", "5432")

**ចំណុចសំខាន់:** default "5432" នៅដដែល → CI មិនត្រូវកែ!
Env var ធ្វើឱ្យ code ដដែល run បាន:
- CI: default 5432 ✅
- ផ្ទះ: DB_PORT=5433 pytest ✅
- Docker network: web→db នៅ 5432 ✅

---

## 📍 ឈុតទី ៣: E302 ជួបលើកទី ៣! + cat > file

កែ app.py → blank lines បាត់ → CI ❌ E302

**ដំណោះស្រាយថ្មី:** ជំនួស file ទាំងមូលដោយ cat > app.py << 'EOF'
— លឿនជាង nano, គ្មានហានិភ័យ paste ខុស!

**ច្បាប់ចាំជារៀងរហូត:** មុន def/@decorator (top-level) =
បន្ទាត់ទទេ ២ ជានិច្ច!

---

## 📍 ឈុតទី ៤: Location-Aware Workflow

    ការិយាល័យ (no Docker) → code, lint, pytest -k "not visits", push
    CI (cloud)             → 8 tests + build + publish GHCR
    ផ្ទះ (Docker)          → integration tests, pull images

Git + CI ភ្ជាប់ទាំង ៣ — គោរព IT policy ការិយាល័យ
ដោយមិនរាំងស្ទះការងារ!

## ✅ លទ្ធផល

- CI ✅ ទាំង 2 jobs — image ថ្មីមាន DB_PORT support នៅ GHCR
- ចេះ debug port conflicts ដោយ netstat + tasklist
- Env vars = code មួយ run គ្រប់ environment (12-factor!)
