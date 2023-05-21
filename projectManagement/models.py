from django.db import models
from django.contrib.auth.models import AbstractUser

class Project(models.Model):
    name = models.CharField(max_length=255)
    description = models.TextField()
    deadline = models.DateTimeField()
    members = models.ManyToManyField(
        AbstractUser,
        through='ProjectMember',
        related_name='projects',
    )
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['-created_at']


class ProjectMember(models.Model):
    PROJECT_ROLE_CHOICES = [
        ('manager', 'Manager'),
        ('worker', 'Worker'),
        ('stakeholder', 'Stakeholder'),
    ]
    user = models.ForeignKey(
        AbstractUser,
        on_delete=models.CASCADE,
        related_name='project_memberships',
    )
    project = models.ForeignKey(
        Project,
        on_delete=models.CASCADE,
        related_name='memberships',
    )
    role = models.CharField(
        max_length=20,
        choices=PROJECT_ROLE_CHOICES,
    )
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        unique_together = ('user', 'project')


class Phase(models.Model):
    name = models.CharField(max_length=255)
    description = models.TextField()
    project = models.ForeignKey(
        Project,
        on_delete=models.CASCADE,
        related_name='phases',
    )
    start_date = models.DateTimeField()
    end_date = models.DateTimeField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['-start_date']


class Unit(models.Model):
    name = models.CharField(max_length=255)
    description = models.TextField()
    deadline = models.DateTimeField()
    phase = models.ForeignKey(
        Phase,
        on_delete=models.CASCADE,
    )
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)


class Task(models.Model):
    name = models.CharField(max_length=255)
    description = models.TextField()
    deadline = models.DateTimeField()
    unit = models.ForeignKey(
        Unit,
        on_delete=models.CASCADE,
    )
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    assigned_users = models.ManyToManyField(
        AbstractUser,
        through='TaskAssignment',
        related_name='task_assignments',
    )

    def is_completed(self):
        if not hasattr(self, '_is_completed'):
            self._is_completed = all(
                task_assignment.is_completed
                for task_assignment in self.taskassignment_set.all()
            )
        return self._is_completed


class TaskAssignment(models.Model):
    task = models.ForeignKey(
        Task,
        on_delete=models.CASCADE,
    )
    user = models.ForeignKey(
        AbstractUser,
        on_delete=models.CASCADE,
        related_name='task_assignments',
    )
    assigned_at = models.DateTimeField(auto_now_add=True)
    is_completed = models.BooleanField(default=False)

    class Meta:
        unique_together = ('task', 'user',)

    def complete(self):
        self.is_completed = True
        self.save()
        if self.task.is_completed():
            # タスクが完了した場合の処理
            pass

