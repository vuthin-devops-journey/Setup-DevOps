# Day 4: GitHub Actions — CI Pipeline ដំបូង

**កាលបរិច្ឆេទ:** 13 សីហា 2026
**ប្រធានបទ:** GitHub Actions, CI (Continuous Integration), Workflow YAML

---

## 🎯 គោលដៅ

- បង្កើត CI pipeline ដំបូងដោយ GitHub Actions
- ឱ្យ tests run ស្វ័យប្រវត្តិរាល់ពេល push ឬបើក PR
- បញ្ជាក់ថា CI ចាប់ code ខូចបានពិតប្រាកដ

---

## 💡 CI ជាអ្វី? ហេតុអ្វីសំខាន់?

**CI (Continuous Integration)** = រាល់ពេល code ថ្មីចូល ត្រូវ test
ស្វ័យប្រវត្តិភ្លាមៗ ដើម្បីឱ្យ main branch ស្អាតជានិច្ច។

**ពីបទពិសោធន៍ផ្ទាល់:** ថ្ងៃមុន merge conflict ធ្វើឱ្យ app.py ខូច
SyntaxError ដោយមិនដឹងខ្លួន។ បើមាន CI តាំងពីដំបូង — robot
នឹងចាប់បានមុនពេល merge!

**លំហូរការងារ:**

    Push code → GitHub ឃើញ workflow file
             → បើក Ubuntu server ថ្មីស្អាត
             → ដំឡើង Python → pip install → pytest
             → ✅ passed ឬ ❌ failed (បង្ហាញក្នុង PR)

---

## 📍 ឈុតទី ១: បង្កើត Workflow File

**ទីតាំងសំខាន់:** `.github/workflows/ci.yml` — GitHub រកតែក្នុង
folder នេះប៉ុណ្ណោះ! ដាក់ខុសកន្លែង = មិនដំណើរការ។

**រចនាសម្ព័ន្ធ ci.yml:**

| ផ្នែក | តួនាទី |
|---|---|
| `name: CI` | ឈ្មោះ workflow |
| `on: push / pull_request → main` | Trigger — run ពេលណា |
| `runs-on: ubuntu-latest` | ប្រើ server Ubuntu របស់ GitHub |
| `actions/checkout@v4` | Clone code ចូល server |
| `actions/setup-python@v5` | ដំឡើង Python 3.12 |
| `pip install -r requirements.txt` | ដំឡើង dependencies |
| `pytest -v` | Run tests |

**ចំណុចសំខាន់:** Steps ក្នុង CI ដូចអ្វីដែលខ្ញុំធ្វើដោយដៃបេះបិទ —
CI គ្រាន់តែយកការងារដដែលៗនោះឱ្យ robot ធ្វើជំនួស!

**ប្រយ័ត្ន:** YAML sensitive ចំពោះ indentation (ដកឃ្លា) —
ខុសមួយកន្លែង workflow មិនដើរទាំងមូល។

---

## 📍 ឈុតទី ២: PR ដំបូងជាមួយ CI

1. Branch `feature/add-ci` → commit → push
2. បង្កើត PR នៅ GitHub
3. ឃើញ 🟡 "checks haven't completed" → រង់ចាំ
4. ✅ "All checks have passed" → Merge!

ចុច Details អាចមើល logs ពេញលេញ — ឃើញ GitHub ដំឡើង Python
និង run pytest ជាផ្ទាល់នៅលើ server គេ។

---

## 📍 ឈុតទី ៣: ការពិសោធន៍ — បំផ្លាញ Code ដោយចេតនា

**អ្វីដែលធ្វើ:**
1. Branch `test/break-ci` → កែ version "1.0.0" → "9.9.9"
2. Push → បង្កើត PR
3. **លទ្ធផល:** ❌ CI Failing!

    AssertionError: assert '9.9.9' == '1.0.0'

**មេរៀន:** CI ចាប់ code ខូចបានពិត — PR បង្ហាញ ❌ ក្រហម
teammates ឃើញភ្លាមថា code នេះ merge មិនបាន។

**សម្អាត:** Close PR (មិន merge) → លុប branch local + remote

---

## 🧠 Concepts & Commands ថ្មី

| ពាក្យ | អត្ថន័យ |
|---|---|
| Workflow | ដំណើរការស្វ័យប្រវត្តិ កំណត់ក្នុង YAML |
| Trigger (`on:`) | ព្រឹត្តិការណ៍ដែលធ្វើឱ្យ workflow run |
| Job | ក្រុមការងារ run លើ server មួយ |
| Step | ជំហានម្តងមួយក្នុង job |
| Runner | Server ដែល run workflow (ubuntu-latest) |
| Action (`uses:`) | Steps សម្រេចស្រាប់ពីគេ (checkout, setup-python) |

| Command | តួនាទី |
|---|---|
| `git branch -D <branch>` | បង្ខំលុប branch មិនទាន់ merge |
| `git push origin --delete <branch>` | លុប branch នៅ remote |

---

## ✅ លទ្ធផលចុងក្រោយ

- CI pipeline ដំណើរការ — tests run ស្វ័យប្រវត្តិគ្រប់ push/PR
- បញ្ជាក់ដោយពិសោធន៍ថា CI ចាប់ code ខូចបាន
- Repo ឥឡូវមាន: app + tests + docs + **CI** 🎉

## 🎯 បន្ទាប់

- បន្ថែម CI badge ចូល README.md
- បន្ថែម linting (flake8) ចូល pipeline
- រៀបចំឆ្ពោះទៅ Docker (សប្តាហ៍ក្រោយ!)
