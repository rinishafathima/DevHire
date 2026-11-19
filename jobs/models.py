from django.db import models
from django.contrib.auth.models import User


class Job(models.Model):
    recruiter = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        null=True,
        blank=True
    )

    title = models.CharField(max_length=200)
    company = models.CharField(max_length=200)
    location = models.CharField(max_length=100)
    salary = models.CharField(max_length=100)
    experience = models.CharField(max_length=100)
    skills = models.CharField(max_length=300)
    description = models.TextField()

    def __str__(self):
        return self.title