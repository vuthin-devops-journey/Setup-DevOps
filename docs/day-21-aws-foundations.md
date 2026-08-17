# Day 21: AWS Foundations — Account, IAM, CLI, S3 ☁️

**កាលបរិច្ឆេទ:** 17 សីហា 2026
**ប្រធានបទ:** AWS account setup, IAM, Access Keys, AWS CLI, S3

---

## 🎯 គោលដៅ

ចាកចេញពី local cluster ទៅ cloud ពិត — ជាមួយវិន័យសុវត្ថិភាព
និងការគ្រប់គ្រងចំណាយតាំងពីថ្ងៃដំបូង។

---

## ⚠️ ការគ្រប់គ្រងចំណាយ (សំខាន់បំផុត!)

| សេវា | Free Tier | ហានិភ័យ |
|---|---|---|
| EC2 t3.micro | 750h/ខែ (12 ខែ) | ✅ បើ 1 instance |
| S3 | 5GB | ✅ |
| RDS db.t3.micro | 750h/ខែ | ⚠️ ភ្លេចលុប = ចំណាយ |
| EKS | ❌ គ្មាន! | 🔴 ~$73/ខែ |
| NAT Gateway | ❌ គ្មាន | 🔴 ~$32/ខែ |

**ច្បាប់មាស:** លុប resources រាល់ពេលរៀនចប់!
**ការពារ:** Zero-spend budget alert → email ពេលចំណាយលើស $0.01

---

## 📍 ឈុតទី ១: Security ជាបឋម

1. **MFA លើ root** — root = អំណាចពេញលេញ, ត្រូវការពារ
2. **IAM user** សម្រាប់ការងារប្រចាំថ្ងៃ (កុំប្រើ root!)
3. **Access keys** សម្រាប់ CLI — secret បង្ហាញតែម្តងគត់
4. **កុំ commit keys ចូល Git!** GitHub scan → hackers → bill រាប់ពាន់

---

## 📍 ឈុតទី ២: បញ្ហាដែលជួប

### 1. Email already associated
AWS មិនផ្ញើ code ថ្មីបើ account មានស្រាប់ — sign in ជំនួស
ឬប្រើ Gmail alias `user+aws@gmail.com`

### 2. `.msi: cannot execute binary file`
`.msi` ជា Windows Installer package មិនមែន executable
**ដំណោះស្រាយ:** `msiexec //i awscli.msi` (slash ពីរក្នុង Git Bash!)

### 3. `Unable to locate credentials`
`aws configure` មិនចប់ — ត្រូវឆ្លងទាំង ៤ prompts
រហូត `$` ត្រឡប់មក (កុំ Ctrl+C!)

### 4. `region_name doesn't match a supported format`
**Debug:** `cat -A ~/.aws/config` — បង្ហាញតួអក្សរលាក់ (^M, spaces)
**មេរៀន:** invisible characters ជាបញ្ហាបុរាណនៅ Windows

### 5. `AccessDenied: s3:ListAllMyBuckets`
IAM user គ្មាន policy!
**មេរៀនធំ — AWS default deny:**

    Authentication (អ្នកជានរណា?) ✅ credentials ត្រឹមត្រូវ
    Authorization (អាចធ្វើអ្វី?) ❌ គ្មាន policy = គ្មានសិទ្ធិ

**អានយល់ error IAM:** `User: <who> is not authorized to
perform: <action>` — ប្រាប់ច្បាស់ថាអ្នកណា ខ្វះសិទ្ធិអ្វី!

---

## 🧠 Commands ថ្មី

| Command | តួនាទី |
|---|---|
| `aws configure` | កំណត់ credentials + region |
| `aws configure list` | មើលការកំណត់បច្ចុប្បន្ន |
| `aws sts get-caller-identity` | "ខ្ញុំជានរណា?" — test credentials |
| `aws s3 mb/ls/cp/rm/rb` | make bucket, list, copy, remove, remove bucket |
| `cat -A <file>` | បង្ហាញតួអក្សរលាក់ (debug!) |

---

## ✅ លទ្ធផល

- AWS account ជាមួយ MFA + budget alert
- IAM user `vuthin-admin` + AdministratorAccess
- AWS CLI configured (region: ap-southeast-1 Singapore)
- S3 bucket ដំបូង → upload → លុប (វិន័យ cleanup!)

## 🎯 បន្ទាប់

- EC2 + VPC + Security Groups (server ពិត)
- RDS PostgreSQL
- Deploy app ទៅ EC2
- EKS — Kubernetes លើ AWS! ☸️☁️
