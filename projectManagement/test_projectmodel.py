from django.test import TestCase
from django.contrib.auth import get_user_model
from .models import Project, ProjectMember

class ProjectTestCase(TestCase):
    def setUp(self):
        self.user = get_user_model().objects.create(username='testuser', password='testpassword')
        self.project = Project.objects.create(
            project_name='test project',
            project_description='test description',
            project_kind='Web',
            responsible=self.user,
            start_day='2023-08-01',
            dead_line='2023-12-01'
        )

    # project_nameが正しく保存されるかテスト
    def test_project_name(self):
        self.assertEqual(self.project.project_name, 'test project')
    
    # generate_joined_idによってユニークなIDが生成されることをテスト
    def test_generate_joined_id(self):
        self.assertNotEqual(self.project.joined_id, '')

    # project_kindが正しく保存されるかテスト
    def test_project_kind(self):
        self.assertEqual(self.project.project_kind, 'Web')

    # responsibleが正しく保存されるかテスト
    def test_responsible(self):
        self.assertEqual(self.project.responsible, self.user)

class ProjectMemberTestCase(TestCase):
    def setUp(self):
        self.user = get_user_model().objects.create(username='testuser', password='testpassword')
        self.project = Project.objects.create(
            project_name='test project',
            project_description='test description',
            project_kind='Web',
            responsible=self.user,
            start_day='2023-08-01',
            dead_line='2023-12-01'
        )
        self.member = ProjectMember.objects.create(
            user=self.user,
            project=self.project,
            role='manager',
            status='joined'
        )

    # userが正しく保存されるかテスト
    def test_user(self):
        self.assertEqual(self.member.user, self.user)

    # projectが正しく保存されるかテスト
    def test_project(self):
        self.assertEqual(self.member.project, self.project)

    # roleが正しく保存されるかテスト
    def test_role(self):
        self.assertEqual(self.member.role, 'manager')

    # statusが正しく保存されるかテスト
    def test_status(self):
        self.assertEqual(self.member.status, 'joined')
