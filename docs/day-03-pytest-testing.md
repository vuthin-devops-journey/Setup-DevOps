# Day 3: Automated Testing ជាមួយ pytest

**កាលបរិច្ឆេទ:** 13 សីហា 2026
**ប្រធានបទ:** pytest, Test Client, Assertions — ការរៀបចំសម្រាប់ CI

---

## 🎯 គោលដៅ

- សរសេរ automated tests សម្រាប់ Flask API ទាំង ៣ endpoints
- យល់ពីមូលហេតុដែល tests ជាបេះដូងរបស់ CI/CD
- បង្កើតទម្លាប់: **code → test → commit** ជានិច្ច

---

## 💡 ហេតុអ្វីត្រូវមាន Tests? (មេរៀនពីបទពិសោធន៍ផ្ទាល់!)

កាលពីថ្ងៃមុន ពេលដោះស្រាយ merge conflict — `app.py` ខូច SyntaxError
ដោយមិនដឹងខ្លួន រហូតដល់ពេល run ទើបឃើញ។

**បើមាន tests + CI:** robot នឹងចាប់ error នោះភ្លាមៗ មុនពេល merge ចូល main
→ main branch ស្អាតជានិច្ច → deploy ដោយទំនុកចិត្ត។

---

## 📍 ឈុតទី ១: បង្កើត test_app.py

**រចនាសម្ព័ន្ធ tests (6 tests):**

| Test | ពិនិត្យអ្វី |
|---|---|
| `test_home_status_code` | GET / → 200 |
| `test_home_message` | GET / → status "running" + មាន message |
| `test_health_status_code` | GET /health → 200 |
| `test_health_response` | GET /health → "healthy" + timestamp |
| `test_version_response` | GET /version → version "1.0.0" |
| `test_not_found` | Route មិនមាន → 404 |

**Concepts សំខាន់:**

- `@pytest.fixture` — រៀបចំ test client ប្រើឡើងវិញគ្រប់ test
- `app.test_client()` — call API ដោយមិនចាំបាច់ run server ពិត (លឿន!)
- `assert` — ពិនិត្យលក្ខខណ្ឌ បើខុស test fail ភ្លាម
- ឈ្មោះ file/function ត្រូវចាប់ផ្តើមដោយ `test_` — pytest រកឃើញស្វ័យប្រវត្តិ

---

## 📍 ឈុតទី ២: Run Tests

```bash
pytest -v
```

**លទ្ធផល:** ✅ 6 passed

---

## 📍 ឈុតទី ៣: ធ្វើឱ្យ Test Fail ដោយចេតនា (ការពិសោធន៍!)

**អ្វីដែលធ្វើ:** កែ version ក្នុង app.py ពី "1.0.0" → "2.0.0"

**លទ្ធផល:**

**មេរៀន:** Test ចាប់បានភ្លាមថា code ប្រែប្រួលខុសពីការរំពឹងទុក។
នេះជាអ្វីដែល CI ធ្វើ — code ខូច = merge មិនបាន!

កែត្រឡប់ "1.0.0" វិញ → 6 passed ✅

---

## 📍 ឈុតទី ៤: Commit តាម Branch Workflow

```bash
git checkout -b feature/add-tests
git add test_app.py
git commit -m "test: add pytest tests for all endpoints"
git push -u origin feature/add-tests
# → GitHub: PR → Merge
git checkout main && git pull origin main
git branch -d feature/add-tests
```

---

## 🧠 Commands ថ្មី

| Command | តួនាទី |
|---|---|
| `pytest` | Run tests ទាំងអស់ |
| `pytest -v` | Run + បង្ហាញលម្អិតម្តងមួយ test |
| `pytest test_app.py::test_home_message` | Run តែ test មួយ |
| `pytest -x` | ឈប់ភ្លាមពេលជួប fail ដំបូង |

---

## ✅ លទ្ធផលចុងក្រោយ

- `test_app.py` មាន 6 tests — ទាំងអស់ passed
- ស្គាល់ concept: fixture, test client, assert
- បញ្ចប់សប្តាហ៍ទី ២ ទាំងស្រុង! 🎉

## 🎯 បន្ទាប់ — សប្តាហ៍ទី ៣: GitHub Actions (CI)

Push code → GitHub run tests ស្វ័យប្រវត្តិលើ server គេ
→ ✅ បៃតង ឬ ❌ ក្រហម — គ្មានការ run tests ដោយដៃទៀតទេ!
