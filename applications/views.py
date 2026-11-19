from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from django.http import JsonResponse
from django.core.mail import send_mail

from .models import Application
from jobs.models import Job


def send_status_update_email(application, new_status):
    """
    Sends personalized, professional emails based on the specific application decision.
    """
    job_title = application.job.title
    company = application.job.company
    candidate_name = application.name

    if new_status == "Selected":
        subject = f"🎉 Congratulations! You have been Selected for {job_title} at {company}"
        message = (
            f"Dear {candidate_name},\n\n"
            f"Congratulations! We are thrilled to inform you that you have been SELECTED for the position of "
            f"{job_title} at {company}!\n\n"
            f"The hiring team was very impressed by your qualifications and interview performance. "
            f"A formal employment offer letter is now ready on your DevHire Candidate Dashboard for your review and digital acceptance.\n\n"
            f"Log in to your dashboard to review compensation and complete next steps:\n"
            f"http://127.0.0.1:8000/dashboard/\n\n"
            f"Warm congratulations,\n"
            f"The DevHire & {company} Recruitment Team"
        )
    elif new_status == "Shortlisted":
        subject = f"⭐ Great News! You are Shortlisted for {job_title} at {company}"
        message = (
            f"Dear {candidate_name},\n\n"
            f"Great news! Your application for {job_title} at {company} has been SHORTLISTED.\n\n"
            f"The hiring manager has reviewed your profile and would like to move forward with the next stage "
            f"of the interview process. Please keep an eye on your inbox ({application.email}) for interview "
            f"scheduling details.\n\n"
            f"You can also track your progress on your DevHire Candidate Dashboard.\n\n"
            f"Best of luck!\n"
            f"DevHire Recruitment Team"
        )
    elif new_status == "Rejected":
        subject = f"Update regarding your application for {job_title} at {company}"
        message = (
            f"Dear {candidate_name},\n\n"
            f"Thank you for taking the time to apply for the {job_title} role at {company} and for your interest "
            f"in joining our team.\n\n"
            f"After careful review of all candidates, we regret to inform you that we have decided to move forward "
            f"with other applicants whose experience more closely matches our current needs.\n\n"
            f"Please know that this was a competitive selection process. We were impressed with your background and "
            f"would love to keep your profile on file for future opportunities that align with your skillset.\n\n"
            f"We encourage you to keep in touch and continue exploring other openings on DevHire. We wish you every "
            f"success in your career journey.\n\n"
            f"Sincerely,\n"
            f"The {company} Talent Acquisition Team\n"
            f"Powered by DevHire"
        )
    elif new_status == "Under Review":
        subject = f"Application Status Update: Under Review - {job_title} at {company}"
        message = (
            f"Dear {candidate_name},\n\n"
            f"We wanted to let you know that your application for {job_title} at {company} is now actively "
            f"UNDER REVIEW by the hiring manager.\n\n"
            f"Our team is screening candidates and will reach out with the next update soon. You can monitor your "
            f"application anytime by logging into your DevHire dashboard.\n\n"
            f"Thank you for your patience,\n"
            f"DevHire Recruitment Team"
        )
    else:
        subject = f"DevHire Application Update - {job_title}"
        message = (
            f"Hello {candidate_name},\n\n"
            f"Your application status for {job_title} at {company} has been updated to: {new_status}.\n\n"
            f"Log in to DevHire to view details.\n\n"
            f"Best regards,\nDevHire Team"
        )

    try:
        send_mail(
            subject=subject,
            message=message,
            from_email="support@devhire.io",
            recipient_list=[application.email],
            fail_silently=True,
        )
    except Exception:
        pass


@login_required
def apply_job(request, job_id):
    job = get_object_or_404(Job, id=job_id)

    # Check if candidate already applied
    existing_application = Application.objects.filter(
        user=request.user,
        job=job,
    ).first()

    if existing_application:
        return render(
            request,
            "applications/already_applied.html",
            {
                "job": job,
                "application": existing_application,
            },
        )

    if request.method == "POST":
        name = request.POST.get("name", "").strip() or request.user.get_full_name() or request.user.username
        email = request.POST.get("email", "").strip() or request.user.email
        phone = request.POST.get("phone", "").strip()
        skills = request.POST.get("skills", "").strip()
        resume = request.FILES.get("resume")
        cover_letter = request.POST.get("cover_letter", "").strip()

        application = Application.objects.create(
            user=request.user,
            job=job,
            name=name,
            email=email,
            phone=phone,
            skills=skills,
            resume=resume,
            cover_letter=cover_letter,
        )

        # 1. Send Application Received Confirmation Email
        try:
            send_mail(
                subject=f"✅ Application Received: {job.title} at {job.company} - DevHire",
                message=(
                    f"Hi {application.name},\n\n"
                    f"Thank you for applying for the position of {job.title} at {job.company} through DevHire!\n\n"
                    f"Your application has been received successfully (Application ID: #{application.id}).\n\n"
                    f"What happens next?\n"
                    f"• The hiring team at {job.company} will review your application and resume.\n"
                    f"• You will receive email notifications as soon as your review status changes.\n"
                    f"• You can also monitor your live status on your DevHire Candidate Dashboard at any time.\n\n"
                    f"We appreciate your interest. Keep in touch, and best of luck with your job search!\n\n"
                    f"Warm regards,\n"
                    f"The DevHire Recruitment Team\n"
                    f"support@devhire.io"
                ),
                from_email="support@devhire.io",
                recipient_list=[application.email],
                fail_silently=True,
            )
        except Exception:
            pass

        return render(
            request,
            "applications/success.html",
            {
                "name": application.name,
                "job": job,
            },
        )

    return render(
        request,
        "applications/apply.html",
        {
            "job": job,
        },
    )


@login_required
def update_application_status(request, application_id):
    application = get_object_or_404(Application, id=application_id)

    # Verify authorization: only the recruiter who posted the job (or superuser) can update status
    if application.job.recruiter != request.user and not request.user.is_superuser:
        return redirect("recruiter_dashboard")

    if request.method == "POST":
        new_status = request.POST.get("status")
        valid_statuses = dict(Application.STATUS_CHOICES)

        if new_status in valid_statuses:
            application.status = new_status
            application.save()

            # Send personalized status decision email (Selected, Shortlisted, Rejected, etc.)
            send_status_update_email(application, new_status)

    return redirect("recruiter_dashboard")


@login_required
def respond_to_offer(request, application_id):
    """
    Candidate accepts or declines the employment offer.
    Updates the database and immediately notifies the Recruiter via email.
    """
    if request.method == "POST":
        application = get_object_or_404(Application, id=application_id, user=request.user)
        decision = request.POST.get("decision", "").strip().lower()

        if decision == "accepted":
            application.status = "Offer Accepted"
        elif decision == "declined":
            application.status = "Offer Declined"
        else:
            return JsonResponse({"status": "error", "message": "Invalid decision"}, status=400)

        application.save()

        # Send alert notification to the recruiter!
        recruiter = application.job.recruiter
        if recruiter and recruiter.email:
            try:
                status_label = "ACCEPTED 🎉" if decision == "accepted" else "DECLINED ❌"
                subject = f"Candidate {status_label} Job Offer: {application.name} for {application.job.title}"
                message = (
                    f"Hello {recruiter.username},\n\n"
                    f"Important recruitment notification on DevHire:\n\n"
                    f"Candidate {application.name} has officially {status_label} the job offer for "
                    f"'{application.job.title}' at {application.job.company}.\n\n"
                    f"Candidate Profile & Contact:\n"
                    f"• Name:  {application.name}\n"
                    f"• Email: {application.email}\n"
                    f"• Phone: {application.phone}\n\n"
                    f"{'Action Required: The candidate is now proceeding through the onboarding roadmap. Please prepare their employment welcome kit.' if decision == 'accepted' else 'You may review other candidates or update the vacancy status from your Recruiter Hub.'}\n\n"
                    f"View full details on your Recruiter Hub:\n"
                    f"http://127.0.0.1:8000/recruiter-dashboard/\n\n"
                    f"Best regards,\n"
                    f"DevHire Recruitment System\n"
                    f"support@devhire.io"
                )
                send_mail(
                    subject=subject,
                    message=message,
                    from_email="support@devhire.io",
                    recipient_list=[recruiter.email],
                    fail_silently=True,
                )
            except Exception:
                pass

        return JsonResponse({
            "status": "success",
            "decision": decision,
            "new_status": application.status,
            "candidate_name": application.name,
            "job_title": application.job.title,
        })

    return JsonResponse({"status": "error", "message": "Method not allowed"}, status=405)
