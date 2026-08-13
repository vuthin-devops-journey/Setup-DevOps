# Day 5: CI Badge + Linting ជាមួយ flake8

**កាលបរិច្ឆេទ:** 13 សីហា 2026
**ប្រធានបទ:** CI Badge, Code Quality, flake8 Linting, README Documentation

---

## 🎯 គោលដៅ

- បន្ថែម CI badge ចូល README ដើម្បីបង្ហាញស្ថានភាព pipeline
- បន្ថែម linting (flake8) ចូល CI — ពិនិត្យគុណភាព code ស្វ័យប្រវត្តិ
- ធ្វើឱ្យ README ក្លាយជា documentation ពេញលេញសម្រាប់ portfolio

---

## 💡 Concepts ថ្មី

### CI Badge ជាអ្វី?

រូបតូចមួយក្នុង README ដែលទាញស្ថានភាព CI ផ្ទាល់ពី GitHub Actions:

- 🟢 passing = main branch ស្អាត tests ទាំងអស់ដើរ
- 🔴 failing = មានអ្វីខូច ត្រូវពិនិត្យ

Repos ល្បីៗទាំងអស់មាន badge — វាបង្ហាញថា project មាន
quality control ពិតប្រាកដ។

**URL pattern:**

    https://github.com/<owner>/<repo>/actions/workflows/ci.yml/badge.svg

### Linting ជាអ្វី? ខុសពី Testing យ៉ាងណា?

| | Testing (pytest) | Linting (flake8) |
|---|---|---|
| ពិនិត្យអ្វី | Code **ដើរត្រឹមត្រូវ**ឬអត់ | Code **សរសេរស្អាត**ឬអត់ |
| ឧទាហរណ៍ចាប់ | `/version` return ខុស | import មិនប្រើ, បន្ទាត់វែងពេក |
| ពេលណា fail | Logic ខុស | Style ខុសស្តង់ដារ (PEP 8) |

**ហេតុអ្វីសំខាន់:** នៅក្រុមហ៊ុន មនុស្សច្រើននាក់សរសេរ code រួមគ្នា —
linting ធានាថា style ដូចគ្នាទាំងអស់ អានងាយ maintain ងាយ។

---

## 📍 ឈុតទី ១: បន្ថែម Badge + កែ README

**អ្វីដែលធ្វើ:**
- បន្ថែម badge នៅជួរលើ README
- បន្ថែម: endpoints table, របៀប run locally, របៀប run tests,
  link ទៅ docs/

**មេរៀន:** README ល្អ = អ្នកចូលមើល repo យល់ក្នុង ៣០ វិនាទី
ថា project នេះជាអ្វី run យ៉ាងម៉េច។ Interviewer មើលនេះមុនគេ!

---

## 📍 ឈុតទី ២: បន្ថែម flake8

**ជំហាន:**
1. បន្ថែម `flake8==7.0.0` ចូល requirements.txt
2. Run local សិន: `flake8 app.py test_app.py --max-line-length=100`
3. គ្មាន output = code ស្អាត ✅

**ទម្លាប់ល្អ:** Run lint នៅ local មុន push ជានិច្ច —
កុំរង់ចាំ CI ប្រាប់ថាខូច ព្រោះខាតពេលរង់ចាំ។

---

## 📍 ឈុតទី ៣: បន្ថែម Lint Step ចូល CI

បន្ថែម step ថ្មីក្នុង `.github/workflows/ci.yml` មុន step tests:

    - name: Lint with flake8
      run: flake8 app.py test_app.py --max-line-length=100

**លំដាប់ pipeline ឥឡូវ:**

    Checkout → Setup Python → Install deps → Lint → Test

**គំនិតសំខាន់:** Lint ដាក់**មុន** test — បើ style ខូច
fail លឿន (fail fast) មិនចាំបាច់ខាតពេល run tests ទេ។

---

## 📍 ឈុតទី ៤: PR + ផ្ទៀងផ្ទាត់

1. Branch `feature/badge-and-lint` → push → PR
2. CI run — ឥឡូវឃើញ steps **Lint + Test** ទាំងពីរ ✅
3. Merge → pull → លុប branch
4. README នៅ GitHub បង្ហាញ badge 🟢 **CI passing**!

---

## 🧠 Commands ថ្មី

| Command | តួនាទី |
|---|---|
| `flake8 <files>` | ពិនិត្យ code style |
| `flake8 --max-line-length=100` | កំណត់ប្រវែងបន្ទាត់អតិបរមា |

---

## ✅ លទ្ធផលចុងក្រោយ

- README professional ជាមួយ badge 🟢
- CI pipeline ពេញលេញ: **Lint → Test**
- បញ្ចប់ Git + CI/CD foundation ទាំងស្រុង! 🎉

## 🎯 បន្ទាប់ — 🐳 Docker!

យក Flask app ដាក់ចូល container:
- សរសេរ Dockerfile ដំបូង
- docker build + docker run
- បញ្ចប់បញ្ហា "works on my machine" ជារៀងរហូត!
