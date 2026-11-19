from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.contrib.auth import logout, authenticate, login

from applications.models import Application
from jobs.models import Job
from .models import RecruiterProfile
from .forms import RegistrationForm


def register(request):
    if request.user.is_authenticated:
        if hasattr(request.user, "recruiterprofile"):
            return redirect("recruiter_dashboard")
        return redirect("dashboard")

    if request.method == "POST":
        form = RegistrationForm(request.POST)
        if form.is_valid():
            user = form.save()
            role = form.cleaned_data.get("role")
            if role == "recruiter":
                company_name = form.cleaned_data.get("company_name", "").strip()
                RecruiterProfile.objects.create(user=user, company_name=company_name)
            
            login(request, user)
            if role == "recruiter":
                return redirect("recruiter_dashboard")
            return redirect("dashboard")
    else:
        form = RegistrationForm()

    return render(request, "accounts/register.html", {"form": form})


def user_login(request):
    if request.user.is_authenticated:
        if hasattr(request.user, "recruiterprofile"):
            return redirect("recruiter_dashboard")
        return redirect("dashboard")

    if request.method == "POST":
        username = request.POST.get("username", "").strip()
        password = request.POST.get("password", "")

        user = authenticate(
            request,
            username=username,
            password=password
        )

        if user is not None:
            login(request, user)
            if hasattr(user, "recruiterprofile"):
                return redirect("recruiter_dashboard")
            return redirect("dashboard")

        return render(
            request,
            "accounts/login.html",
            {
                "error": "Invalid username or password."
            }
        )

    return render(request, "accounts/login.html")


def home(request):
    featured_jobs = Job.objects.all().order_by("-id")[:6]
    return render(request, "accounts/home.html", {"jobs": featured_jobs})


@login_required
def dashboard(request):
    applications = Application.objects.filter(user=request.user).select_related("job").order_by("-applied_at")
    return render(request, "accounts/dashboard.html", {"applications": applications})


@login_required
def recruiter_dashboard(request):
    recruiter_profile = RecruiterProfile.objects.filter(user=request.user).first()
    jobs = Job.objects.filter(recruiter=request.user).order_by("-id")
    applications = Application.objects.filter(job__in=jobs).select_related("job", "user").order_by("-id")
    accepted_offers = applications.filter(status="Offer Accepted")
    declined_offers = applications.filter(status="Offer Declined")
    return render(
        request,
        "accounts/recruiter_dashboard.html",
        {
            "recruiter_profile": recruiter_profile,
            "jobs": jobs,
            "applications": applications,
            "accepted_offers": accepted_offers,
            "declined_offers": declined_offers,
        }
    )


def user_logout(request):
    logout(request)
    return redirect("home")
