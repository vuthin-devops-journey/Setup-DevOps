# Day 8: docker-compose — Flask + PostgreSQL ជាមួយគ្នា 🐳🐘

**កាលបរិច្ឆេទ:** 13 សីហា 2026
**ប្រធានបទ:** docker-compose, Multi-container apps, Environment Variables,
Volumes, Healthchecks, Docker Networking

---

## 🎯 គោលដៅ

- Run app ច្រើន containers (Flask + PostgreSQL) ដោយ command តែមួយ
- បន្ថែម endpoint /visits ដែលរក្សាទុកទិន្នន័យក្នុង database ពិត
- យល់ concepts: service networking, env vars, volumes, healthcheck

---

## 💡 ហេតុអ្វីត្រូវការ docker-compose?

App ពិតមិន run តែឯងទេ — ត្រូវការ database, cache, ។ល។
បើ run ដោយដៃ: docker run db... docker run web... network... 😫

**docker-compose:** ប្រកាសទាំងអស់ក្នុង YAML មួយ →
`docker compose up` → ចប់!

**រចនាសម្ព័ន្ធ project:**

    ┌────────── docker compose up ──────────┐
    │  web (Flask :5000) ──▶ db (Postgres)  │
    │            Docker network              │
    └────────────────────────────────────────┘

---

## 📍 ឈុតទី ១: កែ app.py — Environment Variables

**ចំណុចថ្មីសំខាន់បំផុត:**

    DB_HOST = os.environ.get("DB_HOST", "localhost")

Config (host, user, password) **មិនសរសេរផ្ទាល់ក្នុង code** —
យកពី environment variables ដែល docker-compose ផ្តល់ឱ្យ។

**ហេតុអ្វី?** (12-Factor App principle)
- Code ដដែល run បានគ្រប់ environment (local, staging, production)
- Password មិនជាប់ក្នុង Git
- ប្តូរ config ដោយមិនកែ code

**Endpoint ថ្មី /visits:**
- CREATE TABLE IF NOT EXISTS → INSERT → COUNT
- រាល់ការចូលមើល = +1 ក្នុង PostgreSQL ពិត

---

## 📍 ឈុតទី ២: docker-compose.yml

**រចនាសម្ព័ន្ធ:**

| ផ្នែក | អត្ថន័យ |
|---|---|
| `services: web` | Build ពី Dockerfile យើង + ports + env vars |
| `services: db` | ប្រើ image postgres:16-alpine ស្រាប់ពី Docker Hub |
| `volumes: pgdata` | ទិន្នន័យ db រស់នៅទោះ container លុប |
| `healthcheck` | ពិនិត្យ db ready ដោយ pg_isready |
| `depends_on: condition: service_healthy` | web ចាំ db ready សិនទើប start |

**ចំណុចអស្ចារ្យបំផុត — DB_HOST: db**

Web ភ្ជាប់ database តាមឈ្មោះ `db` — មិនមែន IP ទេ!
docker-compose បង្កើត network ដែល containers ស្គាល់គ្នា
**តាមឈ្មោះ service**។ នេះជា service discovery ដំបូងរបស់ខ្ញុំ —
concept ដដែលនេះនឹងជួបម្តងទៀតក្នុង Kubernetes!

---

## 📍 ឈុតទី ៣: Run + Test

    docker compose up --build

Logs ពី ២ services លាយគ្នា (web-1 | ..., db-1 | ...) —
រង់ចាំ db healthy → web start។

**Test:** http://localhost:5000/visits
- Refresh ទី១ → {"total_visits": 1}
- Refresh ទី២ → {"total_visits": 2} ← ទិន្នន័យក្នុង Postgres ពិត!

---

## 📍 ឈុតទី ៤: ការពិសោធន៍ Volume Persistence

    docker compose down   # លុប containers ទាំងអស់
    docker compose up     # ចាប់ផ្តើមថ្មី

ចូល /visits → **count បន្តពីចាស់** មិនចាប់ពី 1 ទេ!

**មេរៀន:** Container = ephemeral (បាត់បង់បាន) តែ
Volume = persistent (ទិន្នន័យរស់នៅ)។ Database ត្រូវតែមាន volume
— បើគ្មាន ទិន្នន័យបាត់រាល់ពេល container លុប!

---

## 🧠 Commands ថ្មី

| Command | តួនាទី |
|---|---|
| `docker compose up` | Start services ទាំងអស់ |
| `docker compose up --build` | Rebuild image មុន start |
| `docker compose up -d` | Start ក្នុង background |
| `docker compose down` | Stop + លុប containers |
| `docker compose down -v` | + លុប volumes ផង (ទិន្នន័យបាត់!) |
| `docker compose ps` | មើល services status |
| `docker compose logs web` | មើល logs service មួយ |

---

## ✅ លទ្ធផលចុងក្រោយ

- Flask + PostgreSQL run ជាមួយគ្នាដោយ command តែមួយ
- /visits endpoint ជាមួយ database ពិត
- ទិន្នន័យ persistent តាម volume
- Config តាម environment variables (12-factor!)

## 🎯 បន្ទាប់

- CI ជាមួយ database (test /visits ក្នុង GitHub Actions)
- Push image ទៅ container registry
- ឆ្ពោះទៅ Kubernetes! ☸️
