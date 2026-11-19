from django.test import TestCase, Client
from django.urls import reverse
from django.contrib.auth.models import User
from accounts.models import RecruiterProfile
from jobs.models import Job
from .models import Application


class ApplicationsTests(TestCase):
    def setUp(self):
        self.client = Client()
        self.recruiter = User.objects.create_user(
            username="recruiter_corp", password="password123"
        )
        RecruiterProfile.objects.create(user=self.recruiter, company_name="CorpTech")

        self.candidate = User.objects.create_user(
            username="applicant_john", password="password123", email="john@gmail.com"
        )

        self.job = Job.objects.create(
            recruiter=self.recruiter,
            title="Python Engineer",
            company="CorpTech",
            location="Bangalore",
            salary="12 LPA",
            experience="3 years",
            skills="Python, Django",
            description="Backend engineering.",
        )

    def test_apply_job_success(self):
        self.client.login(username="applicant_john", password="password123")
        response = self.client.post(
            reverse("apply_job", kwargs={"job_id": self.job.id}),
            {
                "name": "John Doe",
                "email": "john@gmail.com",
                "phone": "9876543210",
                "skills": "Python, Django",
                "cover_letter": "I am a strong fit.",
            },
        )
        self.assertEqual(response.status_code, 200)
        self.assertTrue(
            Application.objects.filter(user=self.candidate, job=self.job).exists()
        )

    def test_duplicate_application_prevention(self):
        self.client.login(username="applicant_john", password="password123")
        Application.objects.create(
            user=self.candidate,
            job=self.job,
            name="John Doe",
            email="john@gmail.com",
            phone="9876543210",
        )
        # Attempt to access apply page again
        response = self.client.get(reverse("apply_job", kwargs={"job_id": self.job.id}))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Already Applied")
