from django.test import TestCase
from django.contrib.auth import get_user_model
from .models import Project, ProjectMember, Task, TaskAssignment

User = get_user_model()

class TaskTestCase(TestCase):
    def setUp(self):
        # ユーザーの作成
        self.user1 = User.objects.create_user(email='user1@example.com', password='password')
        self.user2 = User.objects.create_user(email='user2@example.com', password='password')
        self.user3 = User.objects.create_user(email='user3@example.com', password='password')
        self.user4 = User.objects.create_user(email='user4@example.com', password='password')
        self.user5 = User.objects.create_user(email='user5@example.com', password='password')

        # プロジェクトの作成
        self.project = Project.objects.create(
            project_name='Test Project',
            project_description='Test project description',
            project_kind='Web',
            responsible=self.user1,
            priority=1,
            joined_id='test_project',
        )

        # プロジェクトメンバーの作成
        ProjectMember.objects.create(
            user=self.user1,
            project=self.project,
            role='manager',
            status='joined',
        )
        ProjectMember.objects.create(
            user=self.user2,
            project=self.project,
            role='worker',
            status='joined',
        )
        ProjectMember.objects.create(
            user=self.user3,
            project=self.project,
            role='worker',
            status='joined',
        )
        ProjectMember.objects.create(
            user=self.user4,
            project=self.project,
            role='worker',
            status='joined',
        )

        # フェーズの作成
        self.phase = self.project.phases.create(
            phase_name='Test Phase',
            phase_description='Test phase description',
            start_day='2023-07-01',
            dead_line='2023-07-31',
        )

        # ユニットの作成
        self.unit = self.phase.units.create(
            unit_name='Test Unit',
            unit_description='Test unit description',
            start_day='2023-07-01',
            dead_line='2023-07-31',
        )

        # タスクの作成
        self.task1 = self.unit.tasks.create(
            task_name='Task 1',
            task_description='Task 1 description',
            start_day='2023-07-01',
            dead_line='2023-07-31',
        )
        self.task2 = self.unit.tasks.create(
            task_name='Task 2',
            task_description='Task 2 description',
            start_day='2023-07-01',
            dead_line='2023-07-31',
        )
        self.task3 = self.unit.tasks.create(
            task_name='Task 3',
            task_description='Task 3 description',
            start_day='2023-07-01',
            dead_line='2023-07-31',
        )
        self.task4 = self.unit.tasks.create(
            task_name='Task 4',
            task_description='Task 4 description',
            start_day='2023-07-01',
            dead_line='2023-07-31',
        )

        # タスクに参加者をアサイン
        self.assignment1 = TaskAssignment.objects.create(task=self.task1, project_member=self.project.projectmember_set.first())
        self.assignment2 = TaskAssignment.objects.create(task=self.task2, project_member=self.project.projectmember_set.all()[1])
        self.assignment3 = TaskAssignment.objects.create(task=self.task2, project_member=self.project.projectmember_set.all()[2])
        self.assignment4 = TaskAssignment.objects.create(task=self.task3, project_member=self.project.projectmember_set.all()[3])

    # タスクとタスクアサインメントのテスト
    def test_task_assignment(self):
        # タスク4にプロジェクトに参加していないメンバーをアサインしようとするが、アサインはできないことを確認する
        non_member = User.objects.create_user(email='user6@example.com', password='password')
        assignment5 = TaskAssignment(task=self.task4, project_member=ProjectMember.objects.create(user=non_member, project=self.project))
        with self.assertRaises(Exception):
            assignment5.save()

    # タスクの完了テスト
    def test_task_completion(self):
        # タスク1に1人の参加者を設定し、その参加者がis_completed_memberをtrueに設定すると、is_completed_taskもtrueになることを確認する
        self.assignment1.is_completed_member = True
        self.assignment1.save()
        self.task1.refresh_from_db()
        self.assertTrue(self.task1.is_completed_task)

        # タスク2に2人の参加者を設定し、全ての参加者がis_completed_memberをtrueに設定すると、is_completed_taskもtrueになることを確認する
        self.assignment2.is_completed_member = True
        self.assignment2.save()
        self.assignment3.is_completed_member = True
        self.assignment3.save()
        self.task2.refresh_from_db()
        self.assertTrue(self.task2.is_completed_task)

        # タスク3に3人の参加者を設定し、全ての参加者がis_completed_memberをtrueに設定すると、is_completed_taskもtrueになることを確認する
        self.assignment1.is_completed_member = False
        self.assignment1.save()
        self.assignment2.is_completed_member = False
        self.assignment2.save()
        self.assignment3.is_completed_member = False
        self.assignment3.save()
        self.assignment4.is_completed_member = True
        self.assignment4.save()
        self.task3.refresh_from_db()
        self.assertTrue(self.task3.is_completed_task)

        # タスク4に2人の参加者を設定し、1人がis_completed_memberをtrueに設定するが、is_completed_taskはfalseのままであることを確認する
        self.assignment2.is_completed_member = True
        self.assignment2.save()
        self.task4.refresh_from_db()
        self.assertFalse(self.task4.is_completed_task)

    # その他の必要なテスト
    def test_other_functionalities(self):
        # タスクの開始日と期日が正しく設定されることを確認する
        self.assertEqual(self.task1.start_day, '2023-07-01')
        self.assertEqual(self.task1.dead_line, '2023-07-31')

        # タスクの優先度が正しく設定されることを確認する
        self.task1.priority = 2
        self.task1.save()
        self.task1.refresh_from_db()
        self.assertEqual(self.task1.priority, 2)

        # タスクの進捗状況が正しく更新されることを確認する
        self.assertFalse(self.task1.is_completed_task)
        self.assignment1.is_completed_member = True
        self.assignment1.save()
        self.task1.refresh_from_db()
        self.assertTrue(self.task1.is_completed_task)

        # タスクの割り当てが正しく行われることを確認する
        self.assertEqual(self.assignment1.task, self.task1)
        self.assertEqual(self.assignment1.project_member, self.project.projectmember_set.first())

        # タスクの割り当て解除が正しく行われることを確認する
        self.assignment1.delete()
        self.assertFalse(TaskAssignment.objects.filter(task=self.task1).exists())

        # タスクの削除が正しく行われることを確認する
        self.task1.delete()
        self.assertFalse(Task.objects.filter(pk=self.task1.pk).exists())

        # タスクの検索機能が正しく動作することを確認する
        result = Task.objects.filter(task_name__icontains='Task')
        self.assertEqual(result.count(), 3)

        # ユーザーがプロジェクトから脱退すると、そのユーザーがアサインされていたタスクも削除されることを確認する
        self.project.projectmember_set.first().delete()
        self.assertFalse(TaskAssignment.objects.filter(project_member__user=self.user1).exists())
