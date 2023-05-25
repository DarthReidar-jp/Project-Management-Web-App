from django.db import models
from django.conf import settings

User = settings.AUTH_USER_MODEL

class Project(models.Model):
    project_name = models.CharField(max_length=255)
    project_description = models.TextField()
    project_kind = models.CharField(max_length=255)#種類を準備する
    responsible = models.ForeignKey(User, on_delete=models.CASCADE)
    priority = models.IntegerField()#優先度を準備する
    invitation_id = models.CharField(max_length=255)
    dead_line = models.DateField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    is_completed_project = models.BooleanField(default=False)

    class Meta:
        ordering = ['-created_at']  # 作成日時の降順でソート
    
    def __str__(self):
        return self.project_name
    
    #ここら辺のコードがうまく働きません
    def save(self, *args, **kwargs):
        if not self.pk or not self.phases.exists():
            self.is_completed_project = False
        elif self.phases.exists() and self.phases.filter(is_completed_phase=False).exists():
            self.is_completed_project = False
        else:
            self.is_completed_project = True
        super().save(*args, **kwargs)


class ProjectMember(models.Model):
    PROJECT_ROLE_CHOICES = [
        ('manager', 'Manager'),  # マネージャー
        ('worker', 'Worker'),  # ワーカー
        ('stakeholder', 'Stakeholder'),  # ステークホルダー
    ]
    user = models.ForeignKey(User,on_delete=models.CASCADE)
    project = models.ForeignKey(Project,on_delete=models.CASCADE)
    role = models.CharField(
        max_length=20,
        choices=PROJECT_ROLE_CHOICES,  # 役割の選択肢
    )
    created_at = models.DateTimeField(auto_now_add=True)  # 作成日時
    updated_at = models.DateTimeField(auto_now=True)  # 更新日時

    class Meta:
        unique_together = ('user', 'project')  # ユーザーとプロジェクトの組み合わせが一意

    def __str__(self):
        return f"{self.user} - {self.project}"

class Phase(models.Model):
    phase_name = models.CharField(max_length=255)
    phase_description = models.TextField()
    project = models.ForeignKey(Project,on_delete=models.CASCADE)  # フェーズが所属するプロジェクト
    start_day = models.DateField()
    dead_line = models.DateField()
    is_completed_phase = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['-start_day']  # 開始日時の降順でソート
    def __str__(self):
        return str(self.phase_name)
    def __str__(self):
        return self.phase_name
    def save(self, *args, **kwargs):
        if not self.pk or not self.units.exists():
            self.is_completed_phase = False
        elif self.units.exists() and self.units.filter(is_completed_unit=False).exists():
            self.is_completed_phase = False
        else:
            self.is_completed_phase = True
        super().save(*args, **kwargs)


class Unit(models.Model):
    unit_name = models.CharField(max_length=255)
    unit_description = models.TextField()
    phase = models.ForeignKey(Phase, on_delete=models.CASCADE)
    start_day = models.DateField()
    dead_line = models.DateField()
    is_completed_unit = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.unit_name
    def save(self, *args, **kwargs):
        if not self.pk or not self.tasks.exists():
            self.is_completed_unit = False
        elif self.tasks.exists() and self.tasks.filter(is_completed_task=False).exists():
            self.is_completed_unit = False
        else:
            self.is_completed_unit = True
        super().save(*args, **kwargs)


class Task(models.Model):
    task_name = models.CharField(max_length=255)
    task_description = models.TextField()
    unit = models.ForeignKey(Unit,on_delete=models.CASCADE,) 
    start_day = models.DateField()
    dead_line = models.DateField()
    is_completed_task = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.task_name
    def save(self, *args, **kwargs):
        if not self.pk or not self.taskassignments.exists():
            self.is_completed_task = False
        elif self.taskassignments.exists() and self.taskassignment.filter(is_completed_taskmember=False).exists():
            self.is_completed_task = False
        else:
            self.is_completed_task = True
        super().save(*args, **kwargs)

class TaskAssignment(models.Model):
    """タスク割り当てモデル"""
    task = models.ForeignKey(Task, on_delete=models.CASCADE)
    project_member = models.ForeignKey(ProjectMember, on_delete=models.CASCADE)
    is_completed_taskmember= models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.task} - {self.project_member}"
