# Day 23: Terraform — Infrastructure as Code 🏗️

**កាលបរិច្ឆេទ:** 18 សីហា 2026
**ប្រធានបទ:** HCL, providers, resources, data sources, state,
lifecycle (init/validate/plan/apply/destroy)

---

## 🎯 បញ្ហាដែល Terraform ដោះស្រាយ

ពី Day 22 (AWS CLI ដោយដៃ):

    ❌ Variables បាត់ ($AMI_ID, $SG_ID) ពេលបិទ terminal
    ❌ Commands វែងៗ ចងចាំមិនបាន
    ❌ AMI ID = None (SSM path ចាស់)
    ❌ SG rule ត្រូវកែរាល់ពេល IP ប្តូរ
    ❌ SSH timeout → ដំឡើង Docker មិនបាន
    ❌ គ្មានប្រវត្តិ → ភ្លេច terminate = ចំណាយ!

ជាមួយ Terraform — **ទាំងអស់ដោះស្រាយក្នុង code:**

    terraform apply    → បង្កើតទាំងអស់
    terraform destroy  → លុបទាំងអស់ក្នុង ១ command 🧹

**គំនិតដដែលនឹង Kubernetes YAML** — ប្រកាស desired state,
tool ធ្វើឱ្យវាកើត។ រៀនម្តង ប្រើច្រើនកន្លែង!

---

## 📍 រចនាសម្ព័ន្ធ Project

| File | តួនាទី |
|---|---|
| providers.tf | Provider config + version constraints + default_tags |
| variables.tf | Inputs (region, instance_type, project_name) |
| main.tf | Resources + data sources |
| outputs.tf | អ្វីដែលបង្ហាញក្រោយ apply |
| .gitignore | **state files មិន commit!** |

`default_tags` ក្នុង provider = tags ដាក់លើគ្រប់ resources
ស្វ័យប្រវត្តិ — រកឃើញងាយថាអ្វីជារបស់ project ណា។

---

## 📍 Data Sources — ដោះស្រាយបញ្ហា Day 22!

    data "aws_ami" "al2023" {
      most_recent = true
      owners      = ["amazon"]
      filter { name = "name"  values = ["al2023-ami-2023*-x86_64"] }
    }

    data "http" "my_ip" { url = "https://checkip.amazonaws.com" }

**Resource vs Data source:**
- `resource` = Terraform **បង្កើត/គ្រប់គ្រង**
- `data` = Terraform **អាន** អ្វីដែលមានស្រាប់

ដោះស្រាយបញ្ហាពិត:
- AMI ID = None → data source រកឯង ថ្មីបំផុតជានិច្ច ✅
- IP ប្តូរ → data source អានឯង → SG rule ត្រឹមត្រូវជានិច្ច ✅

---

## 📍 user_data — Bootstrap ស្វ័យប្រវត្តិ

    user_data = <<-USERDATA
      #!/bin/bash
      dnf install -y docker
      systemctl enable --now docker
      docker run -d -p 80:5000 --restart always \
        ghcr.io/vuthin-devops-journey/setup-devops:latest
    USERDATA

Script run ពេល instance boot — **គ្មាន SSH ត្រូវការ!**
ដោះស្រាយបញ្ហា SSH timeout ពី Day 22 ទាំងស្រុង។

នេះជា **immutable infrastructure** — server configure ខ្លួនឯង
ពេលកើត មិនមែនមនុស្សចូល configure ក្រោយ។

---

## 📍 Lifecycle — វដ្តការងារ

| Command | តួនាទី | ត្រូវការ credentials? |
|---|---|---|
| `terraform init` | ទាញ providers | ❌ (`-backend=false`) |
| `terraform fmt` | រៀបចំ format | ❌ |
| `terraform validate` | ពិនិត្យ syntax + logic | ❌ |
| `terraform plan` | បង្ហាញអ្វីនឹងកើត | ✅ (អានស្ថានភាព cloud) |
| `terraform apply` | បង្កើត/កែ | ✅ |
| `terraform destroy` | លុបទាំងអស់ | ✅ |

**`plan` ជាមិត្តល្អបំផុត** — មិនប៉ះអ្វី គ្រាន់តែបង្ហាញ។
នៅ production ត្រូវ review plan ក្នុង PR មុន apply!

---

## 📍 បទពិសោធន៍ការិយាល័យ — Validate ដោយគ្មាន Credentials

**បញ្ហា:** `terraform plan` → `No valid credential sources found`

**ការវិភាគ:** មិនមែន bug — `plan` ត្រូវការសួរ AWS ថាស្ថានភាព
ពិតជាយ៉ាងណា។ គ្មាន credentials = សួរមិនបាន។

សង្កេត: `data.http.my_ip: Read complete` ✅ — data source
ដែលមិនត្រូវការ AWS ដើរធម្មតា!

**អ្វីដែលធ្វើបាននៅការិយាល័យ:**

    terraform init -backend=false   ✅
    terraform fmt                    ✅
    terraform validate → Success!    ✅

**មេរៀនអាជីព:** នេះជាមូលហេតុ CI pipelines ជាច្រើន run
`validate` លើគ្រប់ PR (លឿន, គ្មាន secrets) រួច `plan`/`apply`
តែលើ main ជាមួយ credentials ដែលរក្សាជា secrets។

---

## 📍 State File — បេះដូង Terraform

`terraform.tfstate` = ការចងចាំរបស់ Terraform អំពីអ្វីដែលវាបង្កើត។
វាភ្ជាប់ code ↔ resources ពិតក្នុង cloud។

**ហេតុអ្វីមិន commit?**
- អាចមាន secrets (passwords, keys ក្នុង resources)
- Conflicts ធ្ងន់ធ្ងរពេលមនុស្សច្រើនធ្វើការព្រមគ្នា

**Production:** remote state ក្នុង S3 + DynamoDB locking
→ ក្រុមចែករំលែក state ដោយសុវត្ថិភាព

---

## 📍 Environment Constraints (មេរៀនអាជីព)

នៅការិយាល័យ: Docker blocked, ខ្លះ domains resolve មិនបាន

    🏢 ការិយាល័យ: សរសេរ code, fmt, validate, docs
    🏠 ផ្ទះ:       plan, apply, destroy
    ☁️ Codespace:  ជម្រើសបម្រុង

**កុំដាក់ AWS credentials លើម៉ាស៊ីនក្រុមហ៊ុន** ដោយគ្មានការអនុញ្ញាត —
credentials អាចបង្កើត resources ចេញវិក្កយបត្រលើ card ផ្ទាល់ខ្លួន
ហើយម៉ាស៊ីនក្រុមហ៊ុនអាចត្រូវ audit/reimage។

**DevOps engineers ល្អ = ចេះធ្វើការក្នុងដែនកំណត់** ដោយបែងចែក
ការងារឱ្យត្រូវកន្លែង មិនមែនតស៊ូជាមួយ IT policy។

---

## ⚠️ វិន័យ Terminal (មេរៀនម្តងទៀត)

Commands ដែលត្រូវការ input ដោយដៃ (`apply`, `destroy` → `yes`)
ឬ run យូរ (`init`, `plan`) — **កុំ paste ជាមួយ commands ផ្សេង!**
Terminal បញ្ជូនបន្ទាត់បន្ទាប់ជាចម្លើយ → លទ្ធផលមិនអាចទាយទុកបាន។

---

## ✅ លទ្ធផល

- Terraform code ពេញលេញក្នុង repo (terraform/)
- ស្គាល់ providers, resources, data sources, outputs, variables
- យល់ state management និងហេតុអ្វីមិន commit
- **validate ជោគជ័យនៅការិយាល័យ ដោយគ្មាន credentials!**

## 🎯 បន្ទាប់

- apply/destroy នៅផ្ទះ → app លើ AWS ដោយ Terraform!
- Remote state (S3 + DynamoDB locking)
- Modules (កូដប្រើឡើងវិញ)
- EKS ជាមួយ Terraform ☸️☁️

---

## 📍 បន្ថែម: Terraform CI + Portfolio README

**Terraform validation workflow** (.github/workflows/terraform.yml):

    on:
      pull_request:
        paths: ['terraform/**']    ← run តែពេល .tf ប្តូរ!
    steps:
      - terraform fmt -check -recursive
      - terraform init -backend=false
      - terraform validate

**ហេតុអ្វីដើរដោយគ្មាន credentials:** `fmt`, `init -backend=false`,
និង `validate` មិនត្អូញត្អែរ AWS — គ្រាន់តែពិនិត្យ syntax និង logic។
នេះជាមូលហេតុ CI ជាច្រើនបំបែក pipeline ជា ២ ដំណាក់:

| ដំណាក់ | Commands | Credentials |
|---|---|---|
| PR | fmt, validate | ❌ មិនត្រូវការ |
| main | plan, apply | ✅ (secrets/OIDC) |

**`paths:` filter** = សន្សំ CI minutes ហើយ pipeline លឿន —
កុំ run terraform checks ពេលកែតែ docs!

**README ធ្វើបច្ចុប្បន្នភាព** ជា portfolio centerpiece:
architecture diagram, stack table, key implementation details,
និងពាក្យបញ្ជា run សម្រាប់គ្រប់ layer (compose, k8s, terraform)។

**មេរៀន documentation:** កត់ត្រានៅពេលមានមេរៀន ឬការរកឃើញ —
មិនមែនរាល់ commit។ docs/ ត្រូវមានតម្លៃក្នុងការអាន មិនមែនតែច្រើន file។
