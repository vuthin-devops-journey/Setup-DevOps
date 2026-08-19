# 📖 Deep Dive ថ្ងៃទី ២ — Docker៖ Image, Layers, និង Container ក្រោម Hood

បន្តពី Deep Dive ទី ១ (Git Internals) — ថ្ងៃនេះឆ្លើយសំណួរ៖ "Image ជាអ្វីពិតប្រាកដ?" "Container ខុសពី VM ត្រង់ណា?" និង "Cache ដំណើរការយ៉ាងម៉េច?"

ធ្វើនៅ Home PC (Docker Desktop) ជាមួយ lab project តូចមួយ (`~/Desktop/docker-lap`)៖ Flask app + requirements.txt + Dockerfile ៥ បន្ទាត់។

---

## 📍 ឈុតទី ០៖ Client ≠ Daemon

ចាប់ផ្តើមភ្លាមជួប error ភ្លាម៖

```
$ docker version --format '{{.Server.Version}}'
error during connect: open //./pipe/dockerDesktopLinuxEngine:
The system cannot find the file specified.
```

ការវិភាគ៖ `docker` CLI ជា **client** ប៉ុណ្ណោះ — command ទាំងអស់ជា HTTP request ទៅ **daemon (engine)**។ Docker Desktop មិនទាន់បើក = daemon អត់មាន = client រកមិនឃើញ pipe។ បើក Docker Desktop → ដំណើរការធម្មតា។

💡 មេរៀន៖ Architecture ពេញ៖ `CLI → REST API → dockerd → containerd → runc → process`

---

## 📍 ឈុតទី ១៖ Digest — SHA ជួបគ្នាម្តងទៀត

```
$ docker pull alpine:3.20
25f1d6b1951a: Pull complete
Digest: sha256:d9e853e87e55526f6b2917df91a2115c36dd7c696a35be12163d44e6e2a4b6bc
```

ការវិភាគ៖ Alpine មាន **layer តែ ១** ហើយ image ទាំងមូលកំណត់ដោយ **digest = SHA-256 នៃ content** — ដូច `git hash-object` ពីម្សិលមិញបេះបិទ។

```
Git:    commit → tree     → blobs
Docker: digest → manifest → layers
```

💡 មេរៀន៖ ពេល build, Docker ក៏បម្លែង tag ទៅ digest ដែរ៖
`python:3.12-slim@sha256:2c941e…` — tag ជាឈ្មោះរំកិលបាន digest ជា content ពិត។

---

## 📍 ឈុតទី ២៖ X-ray image ពិតរបស់ project

`docker history` លើ Flask image ពី CI (tag = Git commit SHA!)៖

```
CMD ["python" "app.py"]      0B      ← metadata
COPY app.py .                1.51kB  ← code យើង!
RUN pip install …            26.1MB  ← dependencies
COPY requirements.txt .      130B
WORKDIR /app                 0B
… (python:3.12 base)         36.8MB  ← 5 days ago
… (Debian base)              78.6MB  ← 2 weeks ago
```

ការវិភាគ៖

- **145MB នៃ image → ~120MB ជា base** — code ពិតប្រាកដតែ 1.51kB!
- Layers **0B** (`CMD`, `ENV`, `EXPOSE`, `WORKDIR`) = metadata មិនប៉ះ filesystem
- Timestamps បង្ហាញស្រទាប់ប្រវត្តិ៖ layers យើង (43h) / python base (5d) / Debian (2w)

💡 មេរៀន៖ លំដាប់ `COPY requirements.txt` → `RUN pip install` → `COPY app.py` មិនមែនចៃដន្យទេ — requirements ប្រែកម្រ ដាក់មុន ដើម្បី cache pip layer (26MB) ជាប់រាល់ CI build។

---

## 📍 ឈុតទី ៣៖ Build ២ ដង — Cache និង Determinism

Build lab image ដំបូង៖ pip step ចំណាយ 4.4s។ Build **ម្តងទៀតដោយមិនកែអ្វី**៖

```
#7 [2/5] WORKDIR /app                 → CACHED
#8 [3/5] COPY requirements.txt .      → CACHED
#9 [4/5] RUN pip install …            → CACHED
#10 [5/5] COPY app.py .               → CACHED
#11 writing image sha256:c44b65761dd4… ← hash ដដែល!
```

ការវិភាគ៖ Cache មិនមែន folder ដាច់ដោយឡែកទេ — **layers ខ្លួនឯងហើយជា cache**។ មុន run step នីមួយៗ Docker សួរ៖ "command ដដែល + files checksum ដដែល?" បាទ → យក layer ចាស់។ Input ដដែល → **image hash ដដែលបេះបិទ** — deterministic ដូច Git។

បន្ទាប់មកកែ `VERSION = "v1"` → `"v2"` ក្នុង app.py រួច build ជា `lab:v2`៖ steps រហូតដល់ pip **នៅ CACHED** — មានតែ `COPY app.py` និងក្រោយវាទើប build ថ្មី។

💡 មេរៀន៖ Layer ណាប្រែ → layers **ក្រោយវាទាំងអស់** build ឡើងវិញ។ Order ក្នុង Dockerfile = លុយ (CI minutes)។

---

## 📍 ឈុតទី ៤៖ Tag = Pointer (ភស្តុតាងពី Docker Desktop)

ក្នុងតារាង Images របស់ Docker Desktop៖

```
lab : v1  →  Image ID c44b65761dd4
lab : v2  →  Image ID 6821bb603e91  ┐
lab : v3  →  Image ID 6821bb603e91  ┘ ដូចគ្នា!
```

ការវិភាគ៖ Build `v3` ដោយមិនកែ content → hash ដដែល → Docker មិន store ស្ទួន គ្រាន់តែបិទ tag ទី ២ លើ image ចាស់។ **Tag = Git branch** — pointer ស្រាលទៅ hash។

`docker system df` បញ្ជាក់ថែម៖ **50 images = 8GB ប៉ុណ្ណោះ** (បើគ្មាន sharing ធំជាងនេះឆ្ងាយ) និង **86 containers = 3.17MB** (~37kB ម្នាក់!)។

💡 មេរៀន៖ Container មិន copy image ទេ — គ្រាន់តែបន្ថែម writable layer ស្តើងមួយពីលើ layers read-only ដែលចែកគ្នា។

---

## 📍 ឈុតទី ៥៖ Container = Process + Namespaces (មិនមែន VM!)

ចូលក្នុង alpine container (Git Bash ត្រូវ `winpty`!)៖

```
$ winpty docker run -it --name deepdive alpine:3.20 sh
/ # ps aux
PID   USER     TIME  COMMAND
    1 root      0:00 sh
    7 root      0:00 ps aux
```

ការវិភាគ៖ **Process ២ ប៉ុណ្ណោះ** — គ្មាន OS, គ្មាន services។ `sh` ឃើញខ្លួនជា **PID 1** ព្រោះ PID namespace — ខាងក្រៅវាជា process ធម្មតាលេខធំ។

💡 មេរៀន៖ PID 1 ជាអ្នកទទួល SIGTERM ពេល K8s terminate pod — ប្រភពនៃ `terminationGracePeriodSeconds`។

---

## 📍 ឈុតទី ៦៖ Host, Port, និង "localhost របស់អ្នកណា?"

Run containers ២ ពី images ខុសគ្នា — ខាងក្នុងទាំងពីរ listen :5000 ដដែល៖

```
$ docker run -d -p 5001:5000 --name lab1 lab:v2
$ docker run -d -p 5002:5000 --name lab2 lab:v1

$ curl -s localhost:5001 && echo && curl -s localhost:5002
{"hostname":"d96096df3c2f","message":"Docker Lab","pid_1_world":1,"version":"v2"}
{"hostname":"9830e45dc142","message":"Docker Lab","pid_1_world":1,"version":"v1"}
```

ការវិភាគ — JSON ២ បន្ទាត់នេះបង្ហាញ namespaces ៣ ព្រមគ្នា៖

| Field | Namespace | អត្ថន័យ |
|---|---|---|
| `version` v2/v1 | mount (filesystem ផ្សេង) | app ២ versions run ព្រមគ្នា — មូលដ្ឋាន blue-green deploy |
| `hostname` = container ID | UTS | container គិតថាខ្លួនជាម៉ាស៊ីនឈ្មោះផ្ទាល់ (K8s: pod name → hostname) |
| `pid_1_world: 1` ទាំងពីរ | PID | ម្នាក់ៗជា PID 1 ក្នុងពិភពរៀងៗខ្លួន |
| ទាំង ២ listen :5000 មិនជាន់ | network | ច្រកចេញ host ខុសគ្នា 5001/5002 |

ចុះអ្នកណាកាន់ port លើ Windows? `netstat` បង្ហាញ PID → `tasklist` បង្ហាញឈ្មោះ៖

```
TCP  0.0.0.0:5001  LISTENING  12528
com.docker.backend.exe  12528
```

ការវិភាគ៖ Windows **មិនដែលឃើញ Flask ទេ** — Flask រស់ក្នុង Linux VM របស់ Docker Desktop។ ផ្លូវ request ពេញ៖

```
Browser → Windows:5001 (com.docker.backend proxy)
        → Linux VM → container network namespace → Flask:5000
```

💡 មេរៀន៖ Flask ត្រូវ listen `0.0.0.0` មិនមែន `127.0.0.1` — បើ listen localhost របស់ container គ្មានអ្នកណា call ចូលបានទេ។ Bug លេខ ១ របស់អ្នកចាប់ផ្តើម Docker!

💡 មេរៀនបន្ថែម៖ `-p 5001:5000` (Docker) = `port: 80 / targetPort: 5000` (K8s Service) = `port-forward 8080:80` — គំនិតដដែល ឈ្មោះផ្សេង។

---

## 🧠 សេចក្តីសង្ខេប — ភ្ជាប់ទៅ DevOps Stack

| Docker concept | លេចឡើងម្តងទៀតនៅ |
|---|---|
| Digest = content hash | Git objects, image tag = commit SHA ក្នុង CI pipeline យើង |
| Layer caching + order | CI build លឿន — pip layer cache ជាប់រាល់ push |
| Tag = pointer | Git branches, Helm `image.tag` ក្នុង values.yaml |
| Namespaces + cgroups | K8s pods, `resources.limits` |
| Writable layer ស្លាប់ជាមួយ container | ហេតុផលដែល PostgreSQL ត្រូវការ PVC ក្នុង K8s |
| PID 1 + SIGTERM | `terminationGracePeriodSeconds`, graceful shutdown |

**Docker គ្មាន magic ទេ — គ្រាន់តែ content-addressed layers + Linux namespaces + cgroups។ ចំណែក "container" គឺ process ធម្មតាដែលពាក់វ៉ែនតាបិទភ្នែក។**

---

## 📌 ចម្លើយ Interview ១ ប្រយោគ

> "Docker packages app + dependencies ជា immutable, content-addressed image រួច run វាជា isolated process ដោយប្រើ Linux namespaces + cgroups — មិនមែន virtualization ទេ។"