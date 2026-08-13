# DevOps Journey 🚀

![CI](https://github.com/vuthin-devops-journey/Setup-DevOps/actions/workflows/ci.yml/badge.svg)

Flask health check API — ការអនុវត្តរៀន DevOps ពី zero ដល់ production។

## Endpoints

| Route | Description |
|---|---|
| `/` | Welcome message |
| `/health` | Health check + timestamp |
| `/version` | App version |

## Run Locally

```bash
python -m venv venv
source venv/Scripts/activate   # Windows Git Bash
pip install -r requirements.txt
python app.py
```

## Run Tests

```bash
pytest -v
```

## Learning Notes

មើលកំណត់ត្រារៀនក្នុង [docs/](docs/)
