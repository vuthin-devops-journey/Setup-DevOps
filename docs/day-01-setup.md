📖 សេណារីយ៉ូមេរៀនថ្ងៃនេះ — ថ្ងៃទី ១-៣៖ ពី Zero ដល់ Flask App + Git

នេះជាសាច់រឿងពេញលេញនៃអ្វីដែលអ្នកបានធ្វើថ្ងៃនេះ (13 សីហា 2026) — រួមទាំងបញ្ហាដែលជួប និងរបៀបដោះស្រាយ ដែលនេះហើយជាការងារ DevOps ពិតប្រាកដ! 😄

🎬 សេណារីយ៉ូ៖ "ការដំឡើងបរិស្ថាន DevOps ដំបូង"

📍 ឈុតទី ១៖ ភ្ជាប់ SSH ទៅ GitHub
គោលដៅ៖ ឱ្យម៉ាស៊ីន Windows អាចទាក់ទង GitHub ដោយសុវត្ថិភាព ដោយមិនចាំបាច់វាយ password។
បញ្ហាដែលជួប៖
git@github.com: Permission denied (publickey)
ការវិភាគ៖ ពិនិត្យ ls ~/.ssh/ ឃើញ key មានរួចហើយ (id_ed25519) — មានន័យថាបញ្ហាមិនមែននៅ local ទេ គឺ key មិនទាន់បាន add ទៅ GitHub។
ដំណោះស្រាយ៖ Copy public key (cat ~/.ssh/id_ed25519.pub) → add ចូល GitHub Settings → SSH keys។
លទ្ធផល៖ ✅ Hi thiravuthin! You've successfully authenticated
💡 មេរៀន៖ SSH key មាន ២ ផ្នែក — private (រក្សាទុកសម្ងាត់) និង public (ចែកបាន)។ Server ស្គាល់យើងតាម public key។


📍 ឈុតទី ២៖ បង្កើត Flask Project
គោលដៅ៖ បង្កើត web API តូចមួយសម្រាប់ប្រើពេញមួយដំណើរ DevOps journey។
Files ដែលបង្កើត៖
File	តួនាទី
app.py	Flask app មាន ២ endpoints: / និង /health
requirements.txt	បញ្ជី dependencies (flask, pytest)
.gitignore	ប្រាប់ Git កុំ track venv/, __pycache__/
ជំនាញថ្មី៖ ប្រើ nano editor — Ctrl+O រក្សាទុក, Ctrl+X ចាកចេញ។


📍 ឈុតទី ៣៖ បញ្ហា Python (Troubleshooting ពិតប្រាកដ!)
បញ្ហាទី ១៖
Python was not found but can be installed from the Microsoft Store
→ Python មិនទាន់ដំឡើង ហើយ Windows មាន "fake alias" បញ្ជូនទៅ Store។
បញ្ហាទី ២៖ winget: command not found → winget មិនមាននៅម៉ាស៊ីននេះ។


បញ្ហាទី ៣៖
curl: (35) schannel: CRYPT_E_NO_REVOCATION_CHECK
→ បញ្ហា SSL revocation check របស់ Windows → ដោះស្រាយដោយ flag --ssl-no-revoke។
ដំណោះស្រាយចុងក្រោយ៖ ដំឡើង Python ដោយ installer + Add to PATH → ✅ venv បង្កើតបាន!
💡 មេរៀន៖ ការងារ DevOps ៨០% គឺ troubleshooting បែបនេះ — អាន error message ឱ្យច្បាស់ → វិភាគមូលហេតុ → សាកល្បងដំណោះស្រាយម្តងមួយៗ។ អ្នកទើបតែធ្វើវាដោយជោគជ័យ!


📍 ឈុតទី ៤៖ Run App ជោគជ័យ! 🎉
bash
python -m venv venv                  # បង្កើតបរិស្ថាន Python ដាច់ដោយឡែក
source venv/Scripts/activate         # ចូលបរិស្ថាននោះ (Windows: Scripts មិនមែន bin)
pip install -r requirements.txt      # ដំឡើង dependencies
python app.py                        # Run server!
លទ្ធផល៖
 * Running on http://127.0.0.1:5000
 * Running on http://172.28.200.93:5000

 
📍 ឈុតទី ៥៖ យល់ដឹង Networking — "localhost ជាអ្វី?"
សំណួរដ៏ល្អដែលអ្នកសួរ! ចម្លើយសង្ខេប៖
Server នោះគឺម៉ាស៊ីនអ្នកផ្ទាល់ — Flask run ក្នុង Git Bash ហើយ browser ជា client
localhost = 127.0.0.1 = ម៉ាស៊ីនខ្លួនឯង (loopback)
172.28.200.93 = Private IP ក្នុង WiFi/LAN
:5000 = Port ដែល Flask ស្តាប់
host="0.0.0.0" = ស្តាប់គ្រប់ interfaces

📍 ឈុតទី ៦៖ Git Commit & Push (កំពុងបន្ត...)
ស្ថានភាពចុងក្រោយ៖
✅ Branch main + commit 5ce500a feat: initial flask health check API
⏳ នៅសល់៖ git remote add origin ... + git push (remote មិនទាន់ភ្ជាប់)
📊 សរុបជំនាញដែលទទួលបានថ្ងៃនេះ
ជំនាញ	ស្ថានភាព
SSH key + GitHub authentication	✅
nano editor	✅
Flask app + REST endpoints	✅
Python venv + pip	✅
Troubleshooting (PATH, SSL, alias)	✅ ពូកែ!
Networking basics (localhost, port, IP)	✅
Git init, add, commit	✅
Git push ទៅ remote	⏳ ថ្ងៃស្អែក
