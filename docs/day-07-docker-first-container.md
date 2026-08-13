# Day 7: Docker — Container ដំបូង! 🐳

**កាលបរិច្ឆេទ:** 13 សីហា 2026
**ប្រធានបទ:** Docker Desktop, WSL 2, Dockerfile, Image vs Container, Port Mapping

---

## 🎯 គោលដៅ

- ដំឡើង Docker Desktop លើ Windows (WSL 2 backend)
- សរសេរ Dockerfile ដំបូង — ដាក់ Flask app ចូល container
- យល់ concepts: image, container, port mapping, layer caching

---

## 💡 ហេតុអ្វី Docker? (ពីបទពិសោធន៍ផ្ទាល់!)

កាលពីថ្ងៃមុន ប្តូរពីម៉ាស៊ីនការិយាល័យទៅម៉ាស៊ីនផ្ទះ — ត្រូវ:
ដំឡើង Python ម្តងទៀត → ដោះស្រាយ PATH ម្តងទៀត → venv ម្តងទៀត
→ pip install ម្តងទៀត... 😫

**ជាមួយ Docker:** ទាំងអស់ខ្ចប់ក្នុង image តែមួយ។
ម៉ាស៊ីនណាមាន Docker → `docker run` → ចប់!

---

## 📍 ឈុតទី ១: ដំឡើង Docker Desktop

**បញ្ហាដែលជួប:**

    error during connect: open //./pipe/dockerDesktopLinuxEngine:
    The system cannot find the file specified

**ការវិភាគ:** Docker CLI មាន (docker --version ដើរ) តែ **Engine
មិនទាន់ run** — Docker Desktop app មិនទាន់បើក!

**រចនាសម្ព័ន្ធ Docker:**

    docker CLI (Git Bash) ──pipe──▶ Docker Engine (Docker Desktop)

**ដំណោះស្រាយ:**
1. `wsl --update` + `wsl --set-default-version 2`
2. បើក Docker Desktop app → រង់ចាំ 🟢 Engine running
3. `docker run hello-world` → ✅ "Hello from Docker!"

**មេរៀន:** docker commands ដើរបានលុះត្រាតែ Docker Desktop បើក!

---

## 📍 ឈុតទី ២: Concepts សំខាន់

| ពាក្យ | ប្រៀបធៀប |
|---|---|
| **Image** | រូបមន្តម្ហូប — template (OS + app + dependencies) |
| **Container** | ម្ហូបឆ្អិនរួច — image ដែលកំពុង run |
| **Docker Hub** | ឃ្លាំង images សាធារណៈ (ដូច GitHub សម្រាប់ images) |
| **Dockerfile** | Script បង្កើត image — "setup ជា code" |

Image មួយ → containers ច្រើន!

---

## 📍 ឈុតទី ៣: សរសេរ Dockerfile

**ចំណុចសំខាន់:** Dockerfile = ជំហាន setup ដែលធ្លាប់ធ្វើដោយដៃ
២ ដងនៅ ២ ម៉ាស៊ីន — សរសេរជា code ម្តងចប់!

| Instruction | ជំនួសការធ្វើដោយដៃ |
|---|---|
| `FROM python:3.12-slim` | ដំឡើង Python + PATH (ឈឺក្បាល ២ ដង!) |
| `WORKDIR /app` | cd ចូល folder |
| `COPY requirements.txt .` + `RUN pip install` | pip install ដោយដៃ |
| `COPY app.py .` | git clone |
| `EXPOSE 5000` | ប្រកាស port |
| `CMD ["python", "app.py"]` | python app.py |

**+ .dockerignore:** venv/, .git/, docs/... មិនចូល image
(ដូច .gitignore តែសម្រាប់ Docker build)

---

## 📍 ឈុតទី ៤: Build + Run

**បញ្ហាតូច:** `docker build` អត់ arguments → error "requires 1 argument"

**ដំណោះស្រាយ:** `docker build -t devops-journey:1.0 .`
- `-t name:version` = tag ឈ្មោះ image
- `.` = build context (folder ដែល Dockerfile នៅ) ← កុំភ្លេច dot!

**អ្វីដែលឃើញ — Layer Caching:**

    #7 COPY requirements.txt .   → CACHED
    #8 RUN pip install ...       → CACHED

Docker មិន rebuild steps ដែលមិនប្រែប្រួល! នេះហើយហេតុអ្វី
COPY requirements.txt ដាក់**មុន** COPY app.py — កែ code
→ rebuild លឿន (pip install ត្រូវ skip)។

**Run:**

    docker run -p 5000:5000 devops-journey:1.0

`-p 5000:5000` = ភ្ជាប់ port Windows → port container
(concept localhost/port ពី Day 1 ត្រឡប់មកវិញ!)

**លទ្ធផល:** Flask app run ក្នុង Linux container —
គ្មាន venv, គ្មាន activate, គ្មានបញ្ហា PATH! 🤯

---

## 🧠 Commands ប្រចាំថ្ងៃ

| Command | តួនាទី |
|---|---|
| `docker build -t name:tag .` | បង្កើត image ពី Dockerfile |
| `docker images` | មើល images ទាំងអស់ |
| `docker run -p H:C image` | Run + map port host:container |
| `docker run -d --name x image` | Run background + ដាក់ឈ្មោះ |
| `docker ps` / `docker ps -a` | មើល containers (running / ទាំងអស់) |
| `docker logs <name>` | មើល logs |
| `docker stop / start <name>` | បញ្ឈប់ / ចាប់ផ្តើម |
| `docker rm <name>` | លុប container |

---

## ✅ លទ្ធផលចុងក្រោយ

- Docker Desktop + WSL 2 ដំណើរការ
- Image `devops-journey:1.0` build ជោគជ័យ
- Flask app run ក្នុង container — ទាំង ៣ endpoints ដើរ!
- Dockerfile + .dockerignore ចូល repo

## 🎯 បន្ទាប់

- docker-compose — run Flask + Database ជាមួយគ្នា
- Push image ទៅ registry តាម
