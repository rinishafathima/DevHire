from rest_framework import serializers
from .models import Application
from jobs.serializers import JobSerializer


class ApplicationSerializer(serializers.ModelSerializer):
    job_details = JobSerializer(source="job", read_only=True)
    applicant_username = serializers.ReadOnlyField(source="user.username")

    class Meta:
        model = Application
        fields = [
            "id",
            "user",
            "applicant_username",
            "job",
            "job_details",
            "name",
            "email",
            "phone",
            "skills",
            "resume",
            "cover_letter",
            "status",
            "applied_at",
        ]
        read_only_fields = ["id", "user", "applicant_username", "status", "applied_at"]
