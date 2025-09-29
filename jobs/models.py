from django.db import models
from django.utils import timezone
from django.core.exceptions import ValidationError


class Job(models.Model):
    class Status(models.TextChoices):
        DRAFT = "draft", "Draft"
        SCHEDULED = "scheduled", "Scheduled"
        IN_PROGRESS = "in_progress", "In Progress"
        COMPLETED = "completed", "Completed"
        CANCELLED = "cancelled", "Cancelled"

    PRIORITY_LEVELS = (
        (1, "Urgent"),
        (2, "High"),
        (3, "Medium"),
        (4, "Low"),
    )
    title = models.CharField(max_length=255)
    description = models.TextField(blank=True)
    client_name = models.CharField(max_length=255)

    created_by = models.ForeignKey(
        "core.CustomUser", related_name="created_jobs", on_delete=models.SET_NULL, null=True, blank=True
    )
    assigned_to = models.ForeignKey(
        "core.CustomUser", related_name="assigned_jobs", on_delete=models.SET_NULL, null=True, blank=True
    )

    status = models.CharField(max_length=30, choices=Status.choices, default=Status.DRAFT)
    priority = models.PositiveSmallIntegerField(choices=PRIORITY_LEVELS, default=2)

    scheduled_date = models.DateField(null=True, blank=True)

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ["-priority", "scheduled_date", "created_at"]

    def __str__(self):
        return f"{self.title} - {self.client_name}"

    def all_tasks_completed(self):
        return not self.tasks.exclude(status=JobTask.Status.COMPLETED).exists()

    def clean(self):
        # Prevent moving to completed if not all tasks complete
        if self.status == self.Status.COMPLETED and not self.all_tasks_completed():
            raise ValidationError("Cannot mark job as completed while some tasks are incomplete.")

    def save(self, *args, **kwargs):
        # enforce clean before saving
        self.full_clean()
        super().save(*args, **kwargs)


class JobTask(models.Model):
    class Status(models.TextChoices):
        UPCOMING = "upcoming", "Upcoming"
        IN_PROGRESS = "in_progress", "In Progress"
        BLOCKED = "blocked", "Blocked"
        COMPLETED = "completed", "Completed"

    job = models.ForeignKey(Job, related_name="tasks", on_delete=models.CASCADE)
    order = models.PositiveIntegerField(default=0, help_text="Lower numbers run earlier")
    required_equipment = models.ManyToManyField(
        "equipment.Equipment", related_name="required_by_tasks", blank=True
    )
    title = models.CharField(max_length=255)
    description = models.TextField(blank=True)
    status = models.CharField(max_length=20, choices=Status.choices, default=Status.UPCOMING)
    completed_at = models.DateTimeField(null=True, blank=True)

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ["order", "created_at"]
        unique_together = (("job", "order"),)

    def __str__(self):
        return f"{self.job.title} - {self.order}: {self.title}"

    def mark_completed(self, by_user=None):
        self.status = self.Status.COMPLETED
        self.completed_at = timezone.now()
        self.save()

        # if the job has all tasks completed, change job status
        job = self.job
        if job.all_tasks_completed():
            job.status = Job.Status.COMPLETED
            job.save()

