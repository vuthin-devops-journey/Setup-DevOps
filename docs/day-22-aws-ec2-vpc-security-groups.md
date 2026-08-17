# Day 22: EC2 + VPC + Security Groups — Server ពិតដំបូង 🖥️☁️

**កាលបរិច្ឆេទ:** 17 សីហា 2026
**ប្រធានបទ:** VPC, Subnets, Security Groups, Key Pairs, AMI, EC2,
Shell variables, AWS CLI query/filter

---

## 🎯 គំនិតស្នូល ៤

    ┌────────── VPC (បណ្តាញឯកជន 10.0.0.0/16) ──────────┐
    │  ┌── Public Subnet ──┐                            │
    │  │  [Security Group] ← firewall កម្រិត instance   │
    │  │    ↓ SSH(22), HTTP(80), App(5000)              │
    │  │  🖥️ EC2 Instance                               │
    │  └────────────────────┘                            │
    │         ↑ Internet Gateway                         │
    └─────────┼─────────────────────────────────────────┘

| គំនិត | ប្រៀបធៀប |
|---|---|
| VPC | បណ្តាញឯកជនក្នុង AWS (ដូច LAN ផ្ទះ) |
| Subnet | ការបែងចែក VPC (public = ចេញ internet) |
| Security Group | Firewall — អនុញ្ញាត ports ណា ពី IP ណា |
| AMI | Machine Image (ដូច Docker image តែសម្រាប់ VM) |
| EC2 | Virtual server |

**ថ្ងៃនេះប្រើ default VPC** ដែល AWS បង្កើតឱ្យស្រាប់ — សាមញ្ញ
និងសុវត្ថិភាព។ ការសាង VPC ខ្លួនឯងជាមេរៀនក្រោយជាមួយ Terraform។

---

## 📍 ឈុតទី ១: Key Pair — SSH Access

    aws ec2 create-key-pair --key-name devops-key \
      --query 'KeyMaterial' --output text > ~/.ssh/devops-key.pem
    chmod 400 ~/.ssh/devops-key.pem

**ចំណុចសំខាន់:** AWS រក្សាតែ public key — private key ផ្តល់ឱ្យ
**តែម្តងគត់** ពេលបង្កើត។ បាត់វា = ចូល server មិនបាន!
`chmod 400` ចាំបាច់ — SSH បដិសេធ key ដែលអានបានដោយអ្នកដទៃ។

---

## 📍 ឈុតទី ២: Security Group — Firewall

    # SSH តែពី IP របស់ខ្ញុំ!
    MY_IP=$(curl -s https://checkip.amazonaws.com)
    aws ec2 authorize-security-group-ingress --group-id $SG_ID \
      --protocol tcp --port 22 --cidr ${MY_IP}/32

    # HTTP + app port សម្រាប់អ្នកទាំងអស់
    ... --port 80 --cidr 0.0.0.0/0
    ... --port 5000 --cidr 0.0.0.0/0

**មេរៀនសុវត្ថិភាពសំខាន់:**

| CIDR | អត្ថន័យ | ប្រើសម្រាប់ |
|---|---|---|
| `1.2.3.4/32` | IP តែមួយ | SSH ✅ |
| `0.0.0.0/0` | ពិភពលោកទាំងមូល | HTTP/HTTPS |

**កុំបើក SSH ទៅ 0.0.0.0/0!** Bots scan internet ២៤/៧ ព្យាយាម
brute force port 22។ នេះជាមូលហេតុមួយនៃការ hack servers ច្រើនបំផុត។

---

## 📍 ឈុតទី ៣: បញ្ហាដែលជួប

### 1. AMI lookup តាម SSM បរាជ័យ → $AMI_ID = None

    aws ssm get-parameters --names /aws/service/ami-amazon-linux-latest/...
    → None

**មូលហេតុ:** AWS ផ្លាស់ប្តូរ SSM parameter paths តាមពេល;
ឯកសារខ្លះចាស់។

**ដំណោះស្រាយ — សួរ AWS ដោយផ្ទាល់:**

    AMI_ID=$(aws ec2 describe-images --owners amazon \
      --filters "Name=name,Values=al2023-ami-2023*-x86_64" \
                "Name=state,Values=available" \
      --query 'sort_by(Images, &CreationDate)[-1].ImageId' \
      --output text)

បំបែក query:
- `--owners amazon` → official AMIs ប៉ុណ្ណោះ (កុំប្រើ owners
  មិនស្គាល់ — អាចមាន malware!)
- `--filters Name=name,Values=...` → ច្រោះតាមឈ្មោះ OS
- `sort_by(Images, &CreationDate)[-1]` → យកថ្មីបំផុត

### 2. `InvalidAMIID.Malformed: Invalid id: "None"`

Variable ទទេ → command បញ្ជូន "None" ទៅ AWS។
**មេរៀន:** ពិនិត្យ variables មុនប្រើ — `echo $VAR` ជានិច្ច!

### 3. `TerminateInstances: No instances specified`

$INSTANCE_ID ទទេ ព្រោះ launch មិនដែលជោគជ័យ។

**មេរៀនស្ងប់ស្ងាត់:** គ្មាន instance = គ្មានចំណាយ ✅
**ការពិនិត្យត្រឹមត្រូវ:**

    aws ec2 describe-instances --query \
      'Reservations[].Instances[].[InstanceId,State.Name]' --output table

---

## 📍 ឈុតទី ៤: Shell Variables បាត់!

Variables (`$AMI_ID`, `$SG_ID`) រស់នៅតែក្នុង terminal session។
បិទ Git Bash → បាត់ → commands បរាជ័យដោយ "None"។

**ដំណោះស្រាយ — file រក្សាទុក:**

    cat > ~/aws-vars.sh << 'INNER'
    export AMI_ID=$(aws ec2 describe-images ...)
    export SG_ID=$(aws ec2 describe-security-groups ...)
    INNER

    # រាល់ពេលបើក terminal ថ្មី:
    source ~/aws-vars.sh

នេះជា pattern ដដែលនឹង `.bashrc` (PATH) និង venv activate —
**ស្ថានភាព session មិនស្ថិតស្ថេរ!**

---

## 📍 ឈុតទី ៥: Launch + SSH

    INSTANCE_ID=$(aws ec2 run-instances \
      --image-id $AMI_ID --instance-type t3.micro \
      --key-name devops-key --security-group-ids $SG_ID \
      --tag-specifications 'ResourceType=instance,Tags=[{Key=Name,Value=devops-server}]' \
      --query 'Instances[0].InstanceId' --output text)

    aws ec2 wait instance-running --instance-ids $INSTANCE_ID
    PUBLIC_IP=$(aws ec2 describe-instances --instance-ids $INSTANCE_ID \
      --query 'Reservations[0].Instances[0].PublicIpAddress' --output text)

    ssh -i ~/.ssh/devops-key.pem ec2-user@$PUBLIC_IP

**`aws ec2 wait`** = command ដ៏មានប្រយោជន៍ — រង់ចាំរហូតដល់ state
ត្រូវ ដោយមិនបាច់ poll ដោយដៃ។ មានសម្រាប់ resources ជាច្រើន
(instance-running, instance-terminated, ...)។

---

## 💰 ឈុតទី ៦: ការគ្រប់គ្រងចំណាយ

| Action | ចំណាយ |
|---|---|
| `stop` | មិនចំណាយ compute តែ EBS នៅ ~$0.08/GB/ខែ |
| `terminate` | លុបទាំងស្រុង — គ្មានចំណាយ ✅ |

**t3.micro** = Free Tier 750h/ខែ (១២ ខែ) — គ្រប់គ្រាន់សម្រាប់
**១ instance** run ២៤/៧។ ២ instances = លើស!

**ទម្លាប់មុនបិទថ្ងៃ:**

    aws ec2 describe-instances --query \
      'Reservations[].Instances[?State.Name==`running`].[InstanceId]' \
      --output table
    → ទទេ = គេងលក់ស្រួល 😴

---

## 🧠 Commands ថ្មី

| Command | តួនាទី |
|---|---|
| `aws ec2 describe-vpcs / describe-subnets` | មើលបណ្តាញ |
| `aws ec2 create-key-pair` | បង្កើត SSH key |
| `aws ec2 create-security-group` | បង្កើត firewall |
| `aws ec2 authorize-security-group-ingress` | បន្ថែម rule |
| `aws ec2 describe-images --owners amazon` | រក AMI |
| `aws ec2 run-instances` | Launch server! |
| `aws ec2 wait instance-running` | រង់ចាំ state |
| `aws ec2 terminate-instances` | លុប |
| `curl -s https://checkip.amazonaws.com` | រក public IP ខ្លួនឯង |

**JMESPath query** (`--query`) = ភាសាច្រោះ JSON ដ៏មានឥទ្ធិពល:
`Reservations[0].Instances[0].PublicIpAddress`,
`sort_by(Images, &CreationDate)[-1]`

---

## ✅ លទ្ធផល

- Key pair + Security Group (SSH restricted to my IP!)
- ស្គាល់ default VPC និង subnets
- ចេះរក AMI ត្រឹមត្រូវដោយ describe-images + sort
- ចេះ debug variables ទទេ និងពិនិត្យ resources មុនចំណាយ

## 🎯 បន្ទាប់

- ដំឡើង Docker លើ EC2 → run app ពី GHCR លើ server ពិត!
- RDS PostgreSQL (managed database)
- EKS — Kubernetes លើ AWS ☸️☁️

---

## 📍 ឈុតបន្ថែម: SSH Timeout — Network Layer Debugging

**បញ្ហា:** `ssh: connect to host ... port 22: Connection timed out`

**ដំណើរ debug:**

1. ពិនិត្យ SG rule → `InvalidPermission.Duplicate` = rule មាន IP
   បច្ចុប្បន្នរួចហើយ ✅ (SG មិនមែនបញ្ហា)
2. Test network path ដោយ curl:

       curl -v telnet://$PUBLIC_IP:22 --max-time 8
       → Connection timed out

3. សន្និដ្ឋាន: packets មិនដល់ = network layer មិនមែន SSH/key

**មូលហេតុទំនងបំផុត:** ISP ឬ network block **outbound port 22**
(policy ការពារ SSH scanning) — កើតឡើងញឹកញាប់នៅ ISP មួយចំនួន
និង corporate networks។

**ដំណោះស្រាយ ៣:**

| វិធី | អត្ថប្រយោជន៍ |
|---|---|
| EC2 Instance Connect (browser) | គ្មាន port 22 ចាំបាច់, ០ setup |
| SSM Session Manager | ឆ្លង port 443, គ្មាន keys, audit log ← **production!** |
| Test port 80 | បញ្ជាក់ថាបញ្ហាជា port 22 ជាក់លាក់ |

**មេរៀនធំ — Session Manager > SSH នៅ production:**
- គ្មាន SSH keys ត្រូវគ្រប់គ្រង/rotate
- គ្មាន inbound ports បើក (SG អាចបិទ 22 ទាំងស្រុង!)
- គ្មាន public IP ចាំបាច់ (instances ក្នុង private subnet)
- Audit log ពេញលេញក្នុង CloudTrail

**Timeout vs Refused (ចាំជានិច្ច):**

    timed out  → packets មិនដល់ → firewall/SG/network layer
    refused    → ដល់ តែគ្មាន service → application layer

---

## 📍 ឈុតបន្ថែម: SSH Timeout — Network Layer Debugging

**បញ្ហា:** `ssh: connect to host ... port 22: Connection timed out`

**ដំណើរ debug:**

1. ពិនិត្យ SG rule → `InvalidPermission.Duplicate` = rule មាន IP
   បច្ចុប្បន្នរួចហើយ ✅ (SG មិនមែនបញ្ហា)
2. Test network path ដោយ curl:

       curl -v telnet://$PUBLIC_IP:22 --max-time 8
       → Connection timed out

3. សន្និដ្ឋាន: packets មិនដល់ = network layer មិនមែន SSH/key

**មូលហេតុទំនងបំផុត:** ISP ឬ network block **outbound port 22**
(policy ការពារ SSH scanning) — កើតឡើងញឹកញាប់នៅ ISP មួយចំនួន
និង corporate networks។

**ដំណោះស្រាយ ៣:**

| វិធី | អត្ថប្រយោជន៍ |
|---|---|
| EC2 Instance Connect (browser) | គ្មាន port 22 ចាំបាច់, ០ setup |
| SSM Session Manager | ឆ្លង port 443, គ្មាន keys, audit log ← **production!** |
| Test port 80 | បញ្ជាក់ថាបញ្ហាជា port 22 ជាក់លាក់ |

**មេរៀនធំ — Session Manager > SSH នៅ production:**
- គ្មាន SSH keys ត្រូវគ្រប់គ្រង/rotate
- គ្មាន inbound ports បើក (SG អាចបិទ 22 ទាំងស្រុង!)
- គ្មាន public IP ចាំបាច់ (instances ក្នុង private subnet)
- Audit log ពេញលេញក្នុង CloudTrail

**Timeout vs Refused (ចាំជានិច្ច):**

    timed out  → packets មិនដល់ → firewall/SG/network layer
    refused    → ដល់ តែគ្មាន service → application layer
