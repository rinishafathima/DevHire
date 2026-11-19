from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.core.mail import send_mail
from .models import Job


def send_new_job_broadcast_alert(job):
    """
    Sends automated Job Alert emails to registered job seekers when a new vacancy is posted.
    """
    # Fetch all candidate users who have an email address
    candidate_emails = list(
        User.objects.filter(recruiterprofile__isnull=True)
        .exclude(email="")
        .values_list("email", flat=True)
    )

    if not candidate_emails:
        return

    try:
        subject = f"⚡ New Tech Opening: {job.title} at {job.company}"
        message = (
            f"Hello,\n\n"
            f"A new developer opening matching your engineering interest was just posted on DevHire!\n\n"
            f"• Position:     {job.title}\n"
            f"• Company:      {job.company}\n"
            f"• Location:     {job.location}\n"
            f"• Compensation: {job.salary}\n"
            f"• Experience:   {job.experience}\n"
            f"• Tech Stack:   {job.skills}\n\n"
            f"Role Preview:\n"
            f"{job.description[:280]}...\n\n"
            f"Log in to DevHire to review requirements and apply:\n"
            f"http://127.0.0.1:8000/jobs/details/{job.id}/\n\n"
            f"Best regards,\n"
            f"The DevHire Recruitment Team\n"
            f"support@devhire.io"
        )
        send_mail(
            subject=subject,
            message=message,
            from_email="support@devhire.io",
            recipient_list=candidate_emails,
            fail_silently=True,
        )
    except Exception:
        pass


def job_list(request):
    search = request.GET.get("search", "").strip()
    location = request.GET.get("location", "").strip()

    jobs = Job.objects.all().order_by("-id")

    if search:
        jobs = jobs.filter(title__icontains=search) | jobs.filter(skills__icontains=search)

    if location:
        jobs = jobs.filter(location__icontains=location)

    return render(
        request,
        "jobs/job_list.html",
        {
            "jobs": jobs,
            "search": search,
            "location": location,
        },
    )


def job_detail(request, job_id):
    job = get_object_or_404(Job, id=job_id)
    return render(request, "jobs/job_detail.html", {"job": job})


@login_required
def add_job(request):
    if not hasattr(request.user, "recruiterprofile"):
        return render(
            request,
            "jobs/add_job.html",
            {
                "error": "Only recruiters can post jobs. Please sign up or log in as a Recruiter."
            },
        )

    default_company = request.user.recruiterprofile.company_name

    if request.method == "POST":
        title = request.POST.get("title", "").strip()
        company = request.POST.get("company", "").strip() or default_company
        location = request.POST.get("location", "").strip()
        salary = request.POST.get("salary", "").strip()
        experience = request.POST.get("experience", "").strip()
        skills = request.POST.get("skills", "").strip()
        description = request.POST.get("description", "").strip()

        if not title:
            return render(
                request,
                "jobs/add_job.html",
                {
                    "error": "Job title is required.",
                    "default_company": default_company,
                },
            )

        new_job = Job.objects.create(
            recruiter=request.user,
            title=title,
            company=company,
            location=location,
            salary=salary,
            experience=experience,
            skills=skills,
            description=description,
        )

        # Notify candidates automatically about the new opening!
        send_new_job_broadcast_alert(new_job)

        return redirect("recruiter_dashboard")

    return render(
        request,
        "jobs/add_job.html",
        {"default_company": default_company},
    )
