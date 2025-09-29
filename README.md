# JobOps System

A Django-based Job Operations Management System with JWT authentication, task scheduling using Celery, and MySQL as the database.

---

## Requirements

- Python 3.9+
- MySQL 8.x
- Redis (for Celery broker & result backend)
- Virtualenv (recommended)

---

## Setup Instructions

### 1. Clone the repository

```bash
git clone https://github.com/AidaKB/job-ops.git
cd job_ops_system
```
## Create and activate virtual environment

```bash
python -m venv venv
# On Windows
venv\Scripts\activate
# On Linux/Mac
source venv/bin/activate
```

## Install dependencies
```bash
pip install -r requirements.txt
```

## Configure environment variables
```bash
DATABASE_NAME=job_ops
DATABASE_USER=
DATABASE_PASS=
DATABASE_HOST=localhost
DATABASE_PORT=
ENV_NAME=dev
SECRET_KEY=
EMAIL_HOST_USER=
EMAIL_HOST_PASSWORD=
DEBUG=True
DJANGO_SETTINGS_MODULE=job_ops_system.settings
REDIS_HOST=127.0.0.1
REDIS_PORT=6379
ALLOWED_HOSTS=*
CORS_ALLOWED_ORIGINS="http://localhost:8000"
```

## Setup database
Make sure MySQL is running, then create the database:

```bash
CREATE DATABASE job_ops
```

## Apply migrations

```bash
python manage.py migrate
```

## Create a superuser:

```bash
python manage.py createsuperuser
```

## Run the development server:

```bash
python manage.py runserver
```

## Start Celery (Task Queue)

Open two terminals:

Terminal 1 – Celery Worker
```bash
celery -A job_ops_system worker -l info
```

Terminal 2 – Celery Beat (Scheduler)
```bash
celery -A job_ops_system beat -l info
```
## API Documentation

```bash
http://localhost:8000/swagger/
```

## Notes

Redis must be running locally at 127.0.0.1:6379

Make sure to start both Celery worker and beat for scheduled tasks to execute
