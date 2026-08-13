# Day 6: ធ្វើការពី ២ ម៉ាស៊ីន + ដោះស្រាយ CI Failure

**កាលបរិច្ឆេទ:** 13 សីហា 2026
**ប្រធានបទ:** Multi-machine workflow, git clone, PATH debugging, flake8 fix

---

## 🎯 គោលដៅ

- បន្តការងារពីម៉ាស៊ីនផ្ទះ (ម៉ាស៊ីនទី ២) ដោយប្រើ Git
- ដោះស្រាយ CI failure (flake8 E302/E305) រហូតដល់ ✅ បៃតង

---

## 📍 ឈុតទី ១: CI Fail ដំបូង (នៅម៉ាស៊ីនការិយាល័យ)

CI ចាប់បាន style errors:

    app.py:6:1: E302 expected 2 blank lines, found 1
    app.py:21:1: E305 expected 2 blank lines after function

**មេរៀន:** PEP 8 តម្រូវបន្ទាត់ទទេ ២ រវាង top-level functions។
CI ធ្វើការពិត — ចាប់បានសូម្បីតែ style តូចតាច!

---

## 📍 ឈុតទី ២: ប្តូរម៉ាស៊ីន — Path ប្រែប្រួល!

**បញ្ហា:** `cd ~/devops-journey` → No such file or directory

**ការវិភាគ:**
- `whoami` → USER (ពីមុន: user)
- `hostname` → asus007-pc (ពីមុន: DESKTOP-OK5RR3K)
- **សន្និដ្ឋាន:** ម៉ាស៊ីនផ្សេង! Code មិននៅទីនេះទេ។

**ដំណោះស្រាយ — Git ជា source of truth:**

    git clone git@github.com:vuthin-devops-journey/Setup-DevOps.git

**មេរៀន:** Code រស់នៅ GitHub — ម៉ាស៊ីនណាក៏ clone បាន។
venv/ មិន clone តាមទេ (.gitignore) — បង្កើតថ្មីពី requirements.txt!

---

## 📍 ឈុតទី ៣: Python PATH Debugging

**បញ្ហា:** Python ដំឡើងរួច (installer បង្ហាញ "Modify Setup")
តែ `python --version` → not found

**ការវិភាគ:** រក python.exe ដោយផ្ទាល់:

    ls "$LOCALAPPDATA/Programs/Python/Python312/python.exe"  → មាន!

**ដំណោះស្រាយ:** Add PATH ចូល ~/.bashrc ជាអចិន្ត្រៃយ៍:

    echo 'export PATH="$LOCALAPPDATA/Programs/Python/Python312:...:$PATH"' >> ~/.bashrc
    source ~/.bashrc

**មេរៀនសំខាន់:**
- PATH = បញ្ជី folders ដែល shell រកកម្មវិធី
- ~/.bashrc = run រាល់ពេលបើក terminal → ការកំណត់ស្ថិតស្ថេរ
- "command not found" ≠ កម្មវិធីគ្មាន — អាចគ្រាន់តែ PATH រកមិនឃើញ

---

## 📍 ឈុតទី ៤: Fix flake8 + Push → CI ✅

1. Setup: venv + pip install + pytest (6 passed)
2. កែ app.py — បន្ទាត់ទទេ ២ រវាង functions
3. ពិនិត្យ local មុន push: flake8 ស្អាត + pytest passed
4. Push → GitHub Actions → ✅ **Lint + Test បៃតងទាំងពីរ!**

**រង្វិលពេញលេញ:**

    Push → CI ❌ → អាន log → ប្តូរម៉ាស៊ីន → clone → setup env
    → fix → test local → push → CI ✅

---

## 🧠 ជំនាញថ្មី

| ជំនាញ | ពិពណ៌នា |
|---|---|
| `git clone` | ទាញ project ពេញលេញពី remote |
| Multi-machine workflow | pull ពេលចាប់ផ្តើម, push ពេលឈប់ |
| PATH + ~/.bashrc | ដោះស្រាយ "command not found" |
| Fail fast | ពិនិត្យ lint/test local មុន push |

## ✅ លទ្ធផល

- ធ្វើការបានពី ២ ម៉ាស៊ីន (ការិយាល័យ + ផ្ទះ)
- CI pipeline ✅ បៃតង — badge passing!
- បញ្ចប់ Git + CI/CD phase ទាំងស្រុង 🎉

## 🎯 បន្ទាប់ — 🐳 Docker!

បញ្ហាដែលជួបថ្ងៃនេះ (ដំឡើង Python, PATH, venv ម្តងទៀតនៅម៉ាស៊ីនថ្មី)
= បញ្ហាដែល Docker ដោះស្រាយ។ Container មួយ run ដូចគ្នាគ្រប់ម៉ាស៊ីន!
