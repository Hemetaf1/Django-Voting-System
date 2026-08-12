# Django-Voting-System

Aftaab is a Django-based project with localization and voting features. This repository is prepared for public sharing while keeping confidential media data and local environment files private.

## What is excluded
- `media/project_images/` is ignored and not tracked by Git.
- Local Python virtual environments `.venv/` and `venv/` are ignored.
- `db.sqlite3` and `.env` secrets are ignored.

## Setup

1. Create and activate a Python virtual environment:

```powershell
python -m venv .venv
.\.venv\Scripts\Activate.ps1
```

2. Install dependencies:

```powershell
pip install -r requirements.txt
```

3. Copy `.env.example` to `.env` or set environment variables manually:

```powershell
copy .env.example .env
```

4. Set environment variables before running the app:

```powershell
$env:DJANGO_SECRET_KEY = "your-secret-key"
$env:DJANGO_DEBUG = "True"
$env:DJANGO_ALLOWED_HOSTS = "localhost,127.0.0.1"
```

5. Run migrations and start the server:

```powershell
python manage.py migrate
python manage.py runserver
```

## Notes for GitHub
- Do not commit real confidential media files.
- Keep `media/project_images/` out of version control.
- Use environment variables for any secret settings.

## Repository name
This project is published under the GitHub repository name `Django-Voting-System`.

