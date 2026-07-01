# GitHub and Railway Deployment Guide

Target GitHub repository:

```text
satyaRaspi/1ssa
```

Repository URL:

```text
https://github.com/satyaRaspi/1ssa
```

## 1. Push to GitHub

Open Terminal from the extracted project folder. Example:

```bash
cd /Users/satyassrinivasan/Desktop/1ss
```

Initialize Git and commit:

```bash
git init
git branch -M main
git add .
git commit -m "Initial Shakti Scheme application deployment"
```

Connect to the GitHub repo:

```bash
git remote add origin https://github.com/satyaRaspi/1ssa.git
```

Push:

```bash
git push -u origin main
```

If `origin` already exists, run:

```bash
git remote set-url origin https://github.com/satyaRaspi/1ssa.git
git push -u origin main
```

## 2. Deploy on Railway from GitHub

1. Open Railway.
2. Create a New Project.
3. Choose **Deploy from GitHub repo**.
4. Select `satyaRaspi/1ssa`.
5. Deploy.
6. In the service settings, open **Networking** and generate a public domain.

Railway will use the included `Dockerfile`. The React frontend is built first and then served by the FastAPI backend as one service.

## 3. Railway persistent storage

For prototype persistence, add a Railway Volume mounted at:

```text
/data
```

Use these variables:

```text
SHAKTI_DB_PATH=/data/shakti_applications.db
SHAKTI_UPLOAD_DIR=/data/uploads
```

The Dockerfile already includes these defaults, but keeping them visible in Railway makes the deployment easier to manage.

## 4. Health checks and test URLs

Railway health check path:

```text
/health
```

After deployment, test:

```text
https://YOUR-RAILWAY-DOMAIN/health
https://YOUR-RAILWAY-DOMAIN/api/version
```

## 5. Default demo login

```text
Username: Admin
Password: admin123
```

Change this before any real pilot.

## 6. Local Docker test

```bash
docker build -t 1ssa .
docker run --rm -p 8000:8000 -e PORT=8000 1ssa
```

Open:

```text
http://localhost:8000
```

## 7. Important production note

SQLite and local file upload storage are acceptable only for prototype use. For production, move citizen data, Aadhaar-related data, proof files, and photographs to a secure production architecture with PostgreSQL, object storage, encryption, audit logs, backup, access control, and retention controls.
