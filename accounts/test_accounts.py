from django.test import TestCase
from django.urls import reverse
from django.contrib.auth import get_user_model
from django.core import mail

User = get_user_model()


class AccountTestCase(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(
            email="testuser@example.com",
            username="testuser",
            first_name="Test",
            last_name="User",
            country="Japan",
            password="testpassword1234"
        )

    def test_user_creation(self):
        self.assertEqual(User.objects.count(), 1)
        self.assertEqual(self.user.email, "testuser@example.com")
        self.assertEqual(self.user.username, "testuser")
        self.assertEqual(self.user.first_name, "Test")
        self.assertEqual(self.user.last_name, "User")
        self.assertEqual(self.user.country, "Japan")

    def test_duplicate_user_creation(self):
        with self.assertRaises(Exception):
            User.objects.create_user(
                email="testuser@example.com",
                username="testuser",
                first_name="Test",
                last_name="User",
                country="Japan",
                password="testpassword1234"
            )

    def test_login(self):
        response = self.client.post(reverse("account_login"), {
            "login": "testuser@example.com",
            "password": "testpassword1234",
        })
        self.assertEqual(response.status_code, 302)  # successful login redirects

    def test_wrong_password_login(self):
        response = self.client.post(reverse("account_login"), {
            "login": "testuser@example.com",
            "password": "wrongpassword",
        })
        self.assertNotEqual(response.status_code, 302)  # unsuccessful login doesn't redirect

    def test_password_reset(self):
        response = self.client.post(reverse("account_reset_password"), {
            "email": "testuser@example.com",
        })
        self.assertEqual(response.status_code, 302)  # successful reset redirects
        self.assertEqual(len(mail.outbox), 1)
        self.assertIn("testuser@example.com", mail.outbox[0].to)
        self.assertIn('reset', mail.outbox[0].body)

    def test_password_reset_for_unregistered_email(self):
        response = self.client.post(reverse("account_reset_password"), {
            "email": "unregistered@example.com",
        })
        self.assertNotEqual(response.status_code, 302)  # unsuccessful reset doesn't redirect
        self.assertEqual(len(mail.outbox), 0)

