
from django.db import models
from django.contrib.auth.models import User
from jobs.models import Job


class Application(models.Model):

    STATUS_CHOICES = [
        ("Pending", "Pending"),
        ("Under Review", "Under Review"),
        ("Shortlisted", "Shortlisted"),
        ("Rejected", "Rejected"),
        ("Selected", "Selected"),
        ("Offer Accepted", "Offer Accepted"),
        ("Offer Declined", "Offer Declined"),
    ]

    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        null=True,
        blank=True
    )

    job = models.ForeignKey(
        Job,
        on_delete=models.CASCADE
    )

    name = models.CharField(max_length=100)
    email = models.EmailField()
    phone = models.CharField(max_length=15)
    skills = models.CharField(max_length=300)

    resume = models.FileField(
        upload_to="resumes/",
        blank=True,
        null=True
    )

    cover_letter = models.TextField(blank=True)

    status = models.CharField(
        max_length=20,
        choices=STATUS_CHOICES,
        default="Pending"
    )

    applied_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.name

