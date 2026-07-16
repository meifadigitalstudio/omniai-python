# OmniAI

AI-powered Business Operating System.

---

## Tech Stack

- FastAPI
- Python
- PostgreSQL
- Redis
- Google Cloud Storage
- Celery

---

## Setup

### Create Virtual Environment

```bash
python -m venv .venv
```

### Activate

PowerShell

```powershell
.\.venv\Scripts\Activate.ps1
```

CMD

```cmd
.venv\Scripts\activate
```

### Install

```bash
pip install -r requirements.txt
```

### Run

```bash
uvicorn app.main:app --reload
```

---

## API Docs

```
http://127.0.0.1:8000/docs
```

---

## Project Structure

```
app/
api/
core/
database/
models/
schemas/
services/
repositories/
middleware/
workers/
ai/
integrations/
utils/
```

---

## Status

Current Phase

- ✅ Project Setup
- ✅ Configuration
- ⏳ Database
- ⏳ Authentication
- ⏳ AI Module
- ⏳ Omnichannel
- ⏳ Chatbot