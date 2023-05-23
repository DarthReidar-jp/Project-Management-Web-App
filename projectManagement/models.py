from django.db import models
from django.conf import settings

User = settings.AUTH_USER_MODEL

class Project(models.Model):
    name = models.CharField(max_length=255)  # プロジェクト名
    description = models.TextField()  # プロジェクトの説明
    deadline = models.DateTimeField()  # プロジェクトの締め切り日時
    members = models.ManyToManyField(
        User,
        through='ProjectMember',
        related_name='projects',  # ユーザーモデルとの多対多関係の関連名
    )
    created_at = models.DateTimeField(auto_now_add=True)  # 作成日時
    updated_at = models.DateTimeField(auto_now=True)  # 更新日時

    class Meta:
        ordering = ['-created_at']  # 作成日時の降順でソート
    def __str__(self):
        return self.name


class ProjectMember(models.Model):
    PROJECT_ROLE_CHOICES = [
        ('manager', 'Manager'),  # マネージャー
        ('worker', 'Worker'),  # ワーカー
        ('stakeholder', 'Stakeholder'),  # ステークホルダー
    ]
    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='project_memberships',  # ユーザーモデルとの関連名
    )
    project = models.ForeignKey(
        Project,
        on_delete=models.CASCADE,
        related_name='memberships',  # プロジェクトモデルとの関連名
    )
    role = models.CharField(
        max_length=20,
        choices=PROJECT_ROLE_CHOICES,  # 役割の選択肢
    )
    created_at = models.DateTimeField(auto_now_add=True)  # 作成日時
    updated_at = models.DateTimeField(auto_now=True)  # 更新日時

    class Meta:
        unique_together = ('user', 'project')  # ユーザーとプロジェクトの組み合わせが一意

    def __str__(self):
        return str(self.user)



class Phase(models.Model):
    name = models.CharField(max_length=255)  # フェーズ名
    description = models.TextField()  # フェーズの説明
    project = models.ForeignKey(
        Project,
        on_delete=models.CASCADE,
        related_name='phases',  # プロジェクトモデルとの関連名
    )  # フェーズが所属するプロジェクト
    start_date = models.DateTimeField()  # フェーズの開始日時
    end_date = models.DateTimeField()  # フェーズの終了日時
    created_at = models.DateTimeField(auto_now_add=True)  # 作成日時
    updated_at = models.DateTimeField(auto_now=True)  # 更新日時

    class Meta:
        ordering = ['-start_date']  # 開始日時の降順でソート
    def __str__(self):
        return str(self.name)


class Unit(models.Model):
    name = models.CharField(max_length=255)  # ユニット名
    description = models.TextField()  # ユニットの説明
    deadline = models.DateTimeField()  # ユニットの締め切り日時
    phase = models.ForeignKey(
        Phase,
        on_delete=models.CASCADE,
    )  # ユニットが所属するフェーズ
    created_at = models.DateTimeField(auto_now_add=True)  # 作成日時
    updated_at = models.DateTimeField(auto_now=True)  # 更新日時
    def __str__(self):
        return str(self.name)


class Task(models.Model):
    name = models.CharField(max_length=255)  # タスク名
    description = models.TextField()  # タスクの説明
    deadline = models.DateTimeField()  # タスクの締め切り日時
    unit = models.ForeignKey(
        Unit,
        on_delete=models.CASCADE,
    )  # タスクが所属するユニット
    created_at = models.DateTimeField(auto_now_add=True)  # 作成日時
    updated_at = models.DateTimeField(auto_now=True)  # 更新日時
    assigned_users = models.ManyToManyField(
        User,
        through='TaskAssignment',
        related_name='assigned_tasks',  # ユーザーモデルとの多対多関係の関連名
    )

    def is_completed(self):
        if not hasattr(self, '_is_completed'):
            # `_is_completed` 属性が存在しない場合の処理
            self._is_completed = all(
                task_assignment.is_completed
                for task_assignment in self.task_assignments.all()
            )
            # タスクに関連する全ての TaskAssignment の完了状態をチェックし、
            # その結果を `_is_completed` 属性に格納する
        return self._is_completed
        # `_is_completed` 属性の値を返す
    def __str__(self):
        return str(self.name)


class TaskAssignment(models.Model):
    task = models.ForeignKey(
        Task,
        on_delete=models.CASCADE,
    )  # 割り当てられたタスク
    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='task_assignments',  # ユーザーモデルとの関連名
    )  # 割り当てられたユーザー
    assigned_at = models.DateTimeField(auto_now_add=True)  # 割り当て日時
    is_completed = models.BooleanField(default=False)  # タスクが完了したかどうか

    class Meta:
        unique_together = ('task', 'user')  # タスクとユーザーの組み合わせは一意

    def complete(self):
        self.is_completed = True  # タスクを完了済みに設定
        self.save()
        if self.task.is_completed():  # タスクが完了した場合
            # タスクが完了した場合の処理
            pass

    def __str__(self):
        return str(self.user)
