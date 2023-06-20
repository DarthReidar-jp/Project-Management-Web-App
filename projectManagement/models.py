from django.db import models
from django.conf import settings

#Account User Substitution
User = settings.AUTH_USER_MODEL

class Project(models.Model):
    project_name = models.CharField(max_length=255)
    project_description = models.TextField()
    project_kind = models.CharField(max_length=255)
    responsible = models.ForeignKey(User, on_delete=models.CASCADE)
    priority = models.IntegerField()
    invitation_id = models.CharField(max_length=255,unique=True)
    dead_line = models.DateField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    is_completed_project = models.BooleanField(default=False)

    class Meta:
        ordering = ['-created_at']
    
    def __str__(self):
        return self.project_name
    
    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)

        phases = self.phases.all()
        if not self.pk or not phases.exists():
            self.is_completed_project = False
        elif phases.exists() and not phases.filter(is_completed_phase=False).exists():
            self.is_completed_project = True
        else:
            self.is_completed_project = False

        self.__class__.objects.filter(pk=self.pk).update(is_completed_project=self.is_completed_project)

class ProjectMember(models.Model):
    PROJECT_ROLE_CHOICES = [
        ('manager', 'Manager'),  # マネージャー
        ('worker', 'Worker'),  # ワーカー
        ('stakeholder', 'Stakeholder'),  # ステークホルダー
    ]
    STATUS_CHOICES = [
        ('applying', '申請中'),
        ('joined', '参加済み'),
    ]
    user = models.ForeignKey(User,on_delete=models.CASCADE)
    project = models.ForeignKey(Project,on_delete=models.CASCADE)
    role = models.CharField(
        max_length=20,
        choices=PROJECT_ROLE_CHOICES,  # 役割の選択肢
    )
    status = models.CharField(
        max_length=20,
        choices=STATUS_CHOICES,
        default='not_participating',
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
    project = models.ForeignKey(Project, on_delete=models.CASCADE, related_name="phases")
    start_day = models.DateField()
    dead_line = models.DateField()
    is_completed_phase = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['-start_day']

    def __str__(self):
        return str(self.phase_name)

    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)

        units = self.units.all()
        if not self.pk or not units.exists():
            self.is_completed_phase = False
        elif units.exists() and not units.filter(is_completed_unit=False).exists():
            self.is_completed_phase = True
        else:
            self.is_completed_phase = False

        self.__class__.objects.filter(pk=self.pk).update(is_completed_phase=self.is_completed_phase)

class Unit(models.Model):
    unit_name = models.CharField(max_length=255)
    unit_description = models.TextField()
    phase = models.ForeignKey(Phase, on_delete=models.CASCADE, related_name="units")
    start_day = models.DateField()
    dead_line = models.DateField()
    is_completed_unit = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.unit_name

    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)

        tasks = self.tasks.all()
        if not self.pk or not tasks.exists():
            self.is_completed_unit = False
        elif tasks.exists() and not tasks.filter(is_completed_task=False).exists():
            self.is_completed_unit = True
        else:
            self.is_completed_unit = False

        self.__class__.objects.filter(pk=self.pk).update(is_completed_unit=self.is_completed_unit)

class Task(models.Model):
    task_name = models.CharField(max_length=255)
    task_description = models.TextField()
    unit = models.ForeignKey(Unit, on_delete=models.CASCADE, related_name="tasks") 
    start_day = models.DateField()
    dead_line = models.DateField()
    is_completed_task = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.task_name

    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)  # 保存処理を先に実行

        assignments = self.assignments.all()
        if not self.pk or not assignments.exists():
            self.is_completed_task = False
        elif assignments.exists() and not assignments.filter(is_completed_member=False).exists():
            self.is_completed_task = True
        else:
            self.is_completed_task = False

        # `is_completed_task`のみを更新
        self.__class__.objects.filter(pk=self.pk).update(is_completed_task=self.is_completed_task)

class TaskAssignment(models.Model):
    """タスク割り当てモデル"""
    task = models.ForeignKey(Task, on_delete=models.CASCADE,related_name="assignments")
    project_member = models.ForeignKey(ProjectMember, on_delete=models.CASCADE)
    is_completed_member= models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.task} - {self.project_member}"
    


