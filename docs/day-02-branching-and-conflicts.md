# Day 2: Branching, Pull Requests & Merge Conflicts

**កាលបរិច្ឆេទ:** 13 សីហា 2026
**ប្រធានបទ:** Git Branching Workflow, PR, Merge Conflicts, Rebase

---

## 🎯 គោលដៅ

- រៀន Git workflow ដូចនៅកន្លែងធ្វើការពិត (branch → PR → merge)
- បង្កើត merge conflict ដោយចេតនា និងដោះស្រាយដោយខ្លួនឯង
- ស្គាល់ rebase និងរបៀបដោះស្រាយ conflict ក្នុង rebase

---

## 📍 ឈុតទី ១: Feature Branch + Pull Request

**អ្វីដែលធ្វើ:**
1. បង្កើត branch `feature/add-version-endpoint`
2. បន្ថែម endpoint `/version` ក្នុង `app.py`
3. Commit + push branch ទៅ GitHub
4. បង្កើត Pull Request → Merge នៅ GitHub
5. `git checkout main` + `git pull origin main`

**មេរៀន:**
- នៅកន្លែងធ្វើការ គេមិន push ចូល main ផ្ទាល់ទេ — ត្រូវឆ្លងកាត់ PR + review
- ពេល checkout branch ផ្សេង files ក្នុង folder ប្តូរតាម branch —
  code មិនបាត់ទេ គ្រាន់តែនៅ branch ផ្សេង

---

## 📍 ឈុតទី ២: បង្កើត Merge Conflict ដោយចេតនា

**អ្វីដែលធ្វើ:**
1. Branch `feature/message-a` — កែ message ជា "Hello from Team A!"
2. Branch `feature/message-b` — កែបន្ទាត់ដដែលជា "Hello from Team B!"
3. Merge A ចូល main → ✅ ជោគជ័យ
4. Merge B ចូល main → 💥 CONFLICT!

**រូបរាង conflict ក្នុង file:**

    <<<<<<< HEAD
    (code នៅ main / Team A)
    =======
    (code ពី branch B)
    >>>>>>> feature/message-b

**របៀបដោះស្រាយ:**
- លុបសញ្ញាទាំង ៣ (`<<<<<<<`, `=======`, `>>>>>>>`)
- រក្សា ឬបញ្ចូល code ដែលចង់បាន → ជ្រើស "Hello from Team A and B!"
- `git add app.py` → `git commit`

---

## 📍 ឈុតទី ៣: បញ្ហាដែលជួប (Troubleshooting ពិត!)

### បញ្ហា ១: SyntaxError ក្រោយដោះស្រាយ conflict

    return jsonify(...)app = Flask(__name__)  ← បន្ទាត់ជាប់គ្នាខុស

**មូលហេតុ:** ពេលលុបសញ្ញា conflict លុបបន្ទាត់ខ្លះច្រើនពេក
**ដំណោះស្រាយ:** សរសេរ app.py ឡើងវិញទាំងមូល
**មេរៀនសំខាន់:** ⚠️ ក្រោយដោះស្រាយ conflict ត្រូវតែ **test មុន commit ជានិច្ច!**

### បញ្ហា ២: Push rejected

    ! [rejected] main -> main (fetch first)

**មូលហេតុ:** GitHub មាន commits (merge PR) ដែល local មិនមាន
**ដំណោះស្រាយ:** `git pull origin main --rebase` រួច push ម្តងទៀត

### បញ្ហា ៣: Conflict ក្នុង rebase (ម្តងហើយម្តងទៀត!)

Rebase replay commits ម្តងមួយៗ — commit ណាប៉ះបន្ទាត់ដដែល conflict ម្តងទៀត។

**លំដាប់ដោះស្រាយ:**
1. `nano app.py` → លុបសញ្ញា conflict → រក្សា code ត្រឹមត្រូវ
2. `git add app.py`
3. `git rebase --continue`
4. បើ editor លេចឡើង (vim) → `Esc` → `:wq` → `Enter`
5. ធ្វើម្តងទៀតរហូតឃើញ "Successfully rebased"

**ផ្លូវរត់គេច:** `git rebase --abort` ត្រឡប់ទៅស្ថានភាពមុន rebase

---

## 🧠 Commands ថ្មីដែលរៀនថ្ងៃនេះ

| Command | តួនាទី |
|---|---|
| `git checkout -b <branch>` | បង្កើត branch ថ្មី + ចូលទៅវា |
| `git branch -a` | មើល branches ទាំងអស់ (local + remote) |
| `git merge <branch>` | បញ្ចូល branch ចូល branch បច្ចុប្បន្ន |
| `git pull --rebase` | ទាញ changes ដោយ replay commits យើងពីលើ |
| `git rebase --continue` | បន្ត rebase ក្រោយដោះស្រាយ conflict |
| `git rebase --abort` | បោះបង់ rebase ត្រឡប់ដើមវិញ |
| `git push origin --delete <branch>` | លុប branch នៅ remote |
| `git fetch --prune` | សម្អាត remote branches ដែលលុបហើយ |

**Vim survival:** `Esc` → `:wq` → `Enter` = save & exit

---

## ✅ លទ្ធផលចុងក្រោយ

- `app.py` មាន ៣ endpoints: `/`, `/health`, `/version`
- ដោះស្រាយ merge conflict បាន ២ ដង (merge ធម្មតា + ក្នុង rebase)
- main branch push ទៅ GitHub ស្អាត

## 🎯 បន្ទាប់

- បន្ថែម tests ដោយ pytest
- GitHub Actions — CI pipeline ដំបូង!
