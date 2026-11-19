from django.test import TestCase, Client
from django.urls import reverse
from django.contrib.auth.models import User
from .models import RecruiterProfile


class AccountsTests(TestCase):
    def setUp(self):
        self.client = Client()
        self.candidate = User.objects.create_user(
            username="testcandidate", password="password123", email="cand@test.com"
        )
        self.recruiter = User.objects.create_user(
            username="testrecruiter", password="password123", email="rec@test.com"
        )
        RecruiterProfile.objects.create(user=self.recruiter, company_name="HireMe Inc")

    def test_candidate_login_redirects_to_candidate_dashboard(self):
        response = self.client.post(
            reverse("login"),
            {"username": "testcandidate", "password": "password123"},
        )
        self.assertRedirects(response, reverse("dashboard"))

    def test_recruiter_login_redirects_to_recruiter_dashboard(self):
        response = self.client.post(
            reverse("login"),
            {"username": "testrecruiter", "password": "password123"},
        )
        self.assertRedirects(response, reverse("recruiter_dashboard"))

    def test_dashboard_requires_login(self):
        response = self.client.get(reverse("dashboard"))
        self.assertEqual(response.status_code, 302)
        self.assertIn("/login/", response.url)

    def test_register_candidate(self):
        response = self.client.post(
            reverse("register"),
            {
                "username": "newuser",
                "email": "new@user.com",
                "password1": "ValidPassword123!",
                "password2": "ValidPassword123!",
                "role": "candidate",
            },
        )
        self.assertTrue(User.objects.filter(username="newuser").exists())
