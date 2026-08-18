# Day 24: Terraform Apply — Infrastructure កើតឡើងពី Code! 🏗️🎉

**កាលបរិច្ឆេទ:** 18 សីហា 2026
**ប្រធានបទ:** terraform apply/destroy lifecycle ពេញលេញលើកដំបូង

---

## 🎯 លទ្ធផលចុងក្រោយ

    terraform apply → yes → រង់ចាំ ~60s
        ↓
    Security Group + EC2 Instance បង្កើតដោយស្វ័យប្រវត្តិ
        ↓
    user_data script ដំណើរការ: dnf install docker →
      systemctl start docker → docker run ghcr.io/.../setup-devops
        ↓
    curl http://<ip>/health
    → {"status":"healthy","timestamp":"2026-08-18T13:11:47"}

**គ្មាន SSH ចូល។ គ្មាន manual step។ ១០០% ស្វ័យប្រវត្តិពី code!**

---

## 📍 វដ្តពេញលេញ

| ជំហាន | Command | លទ្ធផល |
|---|---|---|
| ១ | `terraform init` | ទាញ providers (cached ពីមុន) |
| ២ | `terraform plan` | `Plan: 2 to add, 0 to change, 0 to destroy` |
| ៣ | `terraform apply` → `yes` | Resources បង្កើត + outputs |
| ៤ | `sleep 90` | រង់ចាំ user_data ចប់ |
| ៥ | `curl $(terraform output -raw app_url)` | App healthy! |
| ៦ | `terraform destroy` → `yes` | Resources ទាំងអស់លុប |
| ៧ | `aws ec2 describe-instances` | ផ្ទៀងផ្ទាត់ ០ resources |

---

## 📍 មេរៀនសំខាន់ពី Session នេះ

### Environment issues (terraform command not found)

Terraform ដំឡើងស្រាប់ក្នុង `~/bin/` — តែ PATH មិនត្រូវ persist
រវាង sessions។ ដំណោះស្រាយ: `export PATH` ក្នុង `.bashrc` ជានិច្ច
(pattern ដដែលនឹង Python, minikube, helm ជាដើម)។

**មេរៀនធំ:** local tools ត្រូវការ PATH configuration ជានិច្ច —
នេះជាហេតុផលមួយដែល CI/CD runners (GitHub Actions) ប្រើ tools ស្រាប់
install ដោយស្វ័យប្រវត្តិ ជៀសវាង environment drift។

### terraform output — វិធីមើលលទ្ធផល

    terraform output              → outputs ទាំងអស់
    terraform output <name>       → តម្លៃតែមួយ (មាន quotes)
    terraform output -raw <name>  → តម្លៃដោយគ្មាន quotes (script-friendly!)

`-raw` សំខាន់សម្រាប់ប្រើក្នុង `curl $(terraform output -raw app_url)`
ព្រោះ curl មិនចង់បាន quotes ក្នុង URL។

---

## 🏆 ខ្សែសង្វាក់ IaC ពេញលេញ (ដំណើររយៈពេល ២៤ ថ្ងៃ)

    HCL code (Git)
        ↓ terraform apply
    AWS resources កើតឡើង (EC2, Security Group)
        ↓ user_data bootstrap
    Docker ដំឡើង + container run ស្វ័យប្រវត្តិ
        ↓
    Application healthy — accessible ពីពិភពលោក
        ↓ terraform destroy
    Resources បាត់ទាំងអស់ — ០ ចំណាយបន្ត

**Immutable, reproducible, destroyable — គោលការណ៍ស្នូល IaC!**

---

## ✅ Portfolio ពេញលេញ — ២៤ ថ្ងៃ

    Code → CI/CD → Docker → Registry → Kubernetes → Helm
    → GitOps (ArgoCD) → Monitoring (Prometheus/Grafana)
    → Infrastructure as Code (Terraform) ✅ ចប់ថ្ងៃនេះ!

## 🎯 ជម្រើសបន្ទាប់

- EKS ជាមួយ Terraform (Kubernetes លើ AWS ពិត)
- Remote state (S3 + DynamoDB)
- Job applications — ត្រៀមខ្លួនរួចហើយ!
