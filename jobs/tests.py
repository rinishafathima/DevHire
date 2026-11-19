from django.test import TestCase, Client
from django.urls import reverse
from django.contrib.auth.models import User
from accounts.models import RecruiterProfile
from .models import Job


class JobsTests(TestCase):
    def setUp(self):
        self.client = Client()
        self.recruiter = User.objects.create_user(
            username="recruiter1", password="password123"
        )
        RecruiterProfile.objects.create(user=self.recruiter, company_name="MetaCloud")

        self.candidate = User.objects.create_user(
            username="candidate1", password="password123"
        )

        self.job = Job.objects.create(
            recruiter=self.recruiter,
            title="Django Developer",
            company="MetaCloud",
            location="Remote",
            salary="10 LPA",
            experience="2 years",
            skills="Python, Django, PostgreSQL",
            description="Build scalable APIs.",
        )

    def test_job_list_view(self):
        response = self.client.get(reverse("job_list"))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Django Developer")

    def test_job_search_by_skill(self):
        response = self.client.get(reverse("job_list") + "?search=PostgreSQL")
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Django Developer")

    def test_candidate_cannot_post_job(self):
        self.client.login(username="candidate1", password="password123")
        response = self.client.post(
            reverse("add_job"),
            {
                "title": "Unauthorized Job",
                "company": "Test",
                "location": "Delhi",
                "salary": "5 LPA",
                "experience": "1 yr",
                "skills": "Python",
                "description": "Test",
            },
        )
        self.assertContains(response, "Only recruiters can post jobs")
        self.assertFalse(Job.objects.filter(title="Unauthorized Job").exists())

    def test_api_jobs_list(self):
        response = self.client.get(reverse("api_job_list"))
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json()["count"], 1)
        self.assertEqual(response.json()["results"][0]["title"], "Django Developer")
