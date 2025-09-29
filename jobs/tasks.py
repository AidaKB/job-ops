from celery import shared_task
from django.utils import timezone
from . import models
import logging

logger = logging.getLogger('jobs.tasks')


@shared_task
def flag_overdue_jobs():
    today = timezone.now().date()
    print(f"[DEBUG] Flag overdue jobs task running for {today}")

    overdue_tasks = models.JobTask.objects.filter(
        job__scheduled_date__lt=today,
    ).exclude(status=models.JobTask.Status.COMPLETED)
    print(f"[DEBUG] Found {overdue_tasks.count()} overdue tasks.")

    for task in overdue_tasks:
        job = task.job
        job.is_overdue = True
        job.save()
        logger.info(f"Flagged Job {job.id} as overdue")
