# Git Recovery Lab — Reflog, Rebase Conflict និង Revert

## គោលដៅ (Goal)

អនុវត្តការសង្គ្រោះពីគ្រោះមហន្តរាយ Git ទូទៅ 3 ប្រភេទ នៅក្នុង repo សាកល្បងដាច់ដោយឡែក:
commits បាត់ក្រោយ `reset --hard` ខុស, rebase conflict, និងការ rollback commit ខូច
លើ shared branch (លំនាំ GitOps rollback)។

## អ្វីដែលបានសាងសង់ (What Was Built)

Repo សាកល្បង (`git-practice`) ដែលមាន commit history តូចមួយលើ `app.yaml`,
feature branch ដែលបែកផ្លូវពី `master`, និង commit "deploy ខូច" ក្លែងធ្វើ
លើ shared branch។

## អ្វីដែលខូច (ដោយចេតនា) (What Broke)

1. **Commits បាត់** — run `git reset --hard <old-sha>` ធ្វើឲ្យ commits 2
   រលាយបាត់ពី `git log`។ File ថយក្រោយ ហើយ history មើលទៅដូចជាបាត់ជារៀងរហូត។
2. **Rebase conflict** — `master` (hotfix) និង `feature/add-replicas`
   កែ line ដដែលក្នុង `app.yaml`។ `git rebase master` ឈប់ដោយ
   `CONFLICT (content)` ហើយទុក markers `<<<<<<<` / `=======` / `>>>>>>>`។
3. **Commit ខូចលើ shared branch** — commit `version: 5.0-BROKEN` ទៅ
   `master` ក្លែងធ្វើ image tag ខូចដែល push ទៅ branch ដែល GitOps ឃ្លាំមើល។

## អ្វីដែលចាំបាន (What Stuck)

- Commits ស្ទើរតែមិនដែលបាត់ពិតប្រាកដទេ។ `git log` ដើរតាមខ្សែ parent ពី
  `HEAD` ចុះក្រោមប៉ុណ្ណោះ ចំណែក `git reflog` កត់ត្រាគ្រប់ movement របស់ HEAD
  ដូច្នេះ SHA "បាត់" អាចសង្គ្រោះដោយ `git reset --hard <sha-from-reflog>`។
  (Reflog ជា local-only ហើយផុតកំណត់ ~90 ថ្ងៃ; changes ដែលមិនទាន់ commit
  មិនអាចសង្គ្រោះបានទេ!)
- ក្នុងអំឡុង rebase, `HEAD` ចង្អុលទៅ branch ដែលយើង rebase **ទៅលើ**
  (`master`) មិនមែន branch ខ្លួនឯងទេ — ដូច្នេះក្នុង conflict markers
  ផ្នែក `HEAD` គឺជាការងាររបស់*ភាគីម្ខាងទៀត* ដែលផ្ទុយពីអ្វីដែលគេភាគច្រើនគិត។
- ការដោះស្រាយ conflict មាន 3 ជំហាន: កែ file (ដោះ markers ចេញទាំងអស់),
  `git add`, រួច `git rebase --continue` — **មិនមែន** `git commit` ទេ។
- Rebase សរសេរ history ឡើងវិញ: ការផ្លាស់ប្តូរដដែលទទួល SHA ថ្មី
  (`9764a94` → `9f1c214`)។ នេះជាមូលហេតុដែលមិនត្រូវ rebase branch
  ដែលអ្នកផ្សេង pull រួច។
- លើ shared branch, `git revert` ជាវិធី rollback តែមួយគត់ដែលមានសុវត្ថិភាព:
  វាបន្ថែម commit បញ្ច្រាសថ្មី ជំនួសការកែ history។ Commit ខូចនៅមើលឃើញ
  ក្នុង history ដដែល (audit trail) ខណៈ state ថយក្រោយ។
- ទំនាក់ទំនងជាមួយ GitOps: revert commit ខូចក្នុង repo ដែល ArgoCD ឃ្លាំមើល
  ធ្វើឲ្យ ArgoCD rollback deployment ដោយស្វ័យប្រវត្តិ — Git history
  *គឺជា* deployment history ដោយមិនចាំបាច់ `kubectl` ដោយដៃ។
- ពេលវង្វេងកណ្តាល operation, run `git status` មុនគេ។ វាប្រាប់ច្បាស់ថា
  កំពុងនៅស្ថានភាពណា ហើយ command ណាដែលត្រូវប្រើ (រៀនពីបទពិសោធន៍ផ្ទាល់
  ពេល `rebase --continue` រំលង ហើយ log មើលទៅដូចជា "ជាប់គាំង")។

## Commands សំខាន់ (Key Commands)

```bash
git reflog                      # គ្រប់កន្លែងដែល HEAD ធ្លាប់ទៅ (ផែនទីសង្គ្រោះ)
git reset --hard <sha>          # ផ្លាស់ branch ទៅ sha (LOCAL branches ប៉ុណ្ណោះ)
git rebase master               # ដាក់ commits របស់ branch លើចុង master
git rebase --continue           # ក្រោយដោះស្រាយ conflict + git add
git rebase --abort              # បោះបង់ ត្រឡប់ទៅស្ថានភាពមុន rebase
git revert <sha> --no-edit      # rollback មានសុវត្ថិភាពលើ shared branches
git status                      # command ដំបូងពេលវង្វេង ឬជាប់គាំង
git log --oneline --graph --all # មើល branch topology
```

## ច្បាប់សម្រេចចិត្ត (Decision Rule)

- មិនទាន់ push / គ្មាននរណា pull → `reset` ឬ `rebase` បានសេរី
- Push រួច ហើយ shared → `revert` **តែប៉ុណ្ណោះ**
- វង្វេង → `git status` មុនគេ រួច `reflog` ជា safety net
