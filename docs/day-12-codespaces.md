# Day 12: GitHub Codespaces — Docker នៅការិយាល័យតាម Browser! ☁️

**កាលបរិច្ឆេទ:** 14 សីហា 2026

## 📍 បញ្ហា: ការិយាល័យគ្មាន Docker

- Docker Desktop → មិនអនុញ្ញាត (error 500 = គ្មាន engine)
- Codespaces លើ org repo → disabled
- Fork → disabled → ជា org owner → បើក settings → fork ដើរ!

## 📍 ដំណោះស្រាយ: Fork → Personal Codespace

Fork ទៅ thiravuthin/Setup-DevOps → Code → Codespaces →
Create → VS Code + Linux VM + Docker ក្នុង browser (free 120h/ខែ)

## 📍 Errors 3 + ដំណោះស្រាយ (Debugging Chain!)

**1. Connection refused (pytest)**
→ ភ្លេច start db! docker compose up -d db
→ មេរៀន: refused = គ្មាន server / auth failed = server ខុស

**2. HTTP 502 (browser)**
→ បើក port 5433 (Postgres) ជំនួស 5000 (Flask)
→ មេរៀន: db port មិននិយាយ HTTP!

**3. localhost:5000 refused (browser Windows)**
→ localhost browser = Windows, app នៅ Codespace VM!
→ ដំណោះស្រាយ: PORTS tab → 5000 → 🌐 GitHub tunnel URL
→ មេរៀន: localhost ជារបស់ម៉ាស៊ីននីមួយៗ

**4. Bonus — pytest នៅ fail ទោះ db run**
→ compose map "5433:5432" ដើរតាម Git គ្រប់ម៉ាស៊ីន!
→ DB_PORT=5433 pytest -v → 8 passed! ✅
→ មេរៀន: Trust the output (docker compose ps) not assumptions!

## 📍 Port Map ត្រឹមត្រូវចុងក្រោយ

    ផ្ទះ + Codespace: DB_PORT=5433 (compose map)
    CI:               5432 (ci.yml service ផ្ទាល់)
    web → db:         5432 (Docker network ខាងក្នុង)

## ✅ លទ្ធផល

- Docker labs នៅការិយាល័យតាម browser — ជារៀងរហូត!
- 8 passed ក្នុង Codespace ☁️
- App public URL តាម GitHub port forwarding
  (concept ដដែលនឹងជួបក្នុង kubectl port-forward!)
