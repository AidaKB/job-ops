import os
from celery import Celery

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'job_ops_system.settings')

app = Celery('job_ops_system')
app.config_from_object('django.conf:settings', namespace='CELERY')
app.autodiscover_tasks()


app.conf.beat_schedule = {
    'flag-overdue-tasks-every-1-min': {
        'task': 'jobs.tasks.flag_overdue_jobs',
        'schedule': 60.0,
    },
}