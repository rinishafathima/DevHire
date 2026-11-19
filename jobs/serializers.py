from rest_framework import serializers
from .models import Job


class JobSerializer(serializers.ModelSerializer):
    recruiter_username = serializers.ReadOnlyField(source="recruiter.username")

    class Meta:
        model = Job
        fields = [
            "id",
            "recruiter",
            "recruiter_username",
            "title",
            "company",
            "location",
            "salary",
            "experience",
            "skills",
            "description",
        ]
        read_only_fields = ["id", "recruiter", "recruiter_username"]
