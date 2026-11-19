from django import forms
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm
from .models import RecruiterProfile


class RegistrationForm(UserCreationForm):
    ROLE_CHOICES = [
        ("candidate", "Job Seeker / Candidate"),
        ("recruiter", "Recruiter / Employer"),
    ]
    role = forms.ChoiceField(
        choices=ROLE_CHOICES,
        widget=forms.RadioSelect,
        initial="candidate",
        help_text="Select your account type",
    )
    email = forms.EmailField(required=True, help_text="Required for notifications")
    company_name = forms.CharField(
        max_length=150,
        required=False,
        help_text="Required only if registering as a Recruiter",
    )

    class Meta(UserCreationForm.Meta):
        model = User
        fields = ("username", "email")

    def clean(self):
        cleaned_data = super().clean()
        role = cleaned_data.get("role")
        company_name = cleaned_data.get("company_name", "").strip()

        if role == "recruiter" and not company_name:
            self.add_error("company_name", "Company name is required for recruiter accounts.")

        return cleaned_data
