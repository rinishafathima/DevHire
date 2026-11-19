import os
import django

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "smartjob.settings")
django.setup()

from django.contrib.auth.models import User
from accounts.models import RecruiterProfile
from jobs.models import Job
from applications.models import Application


def seed_data():
    print("Clearing old demo data...")
    # Keep it clean
    Application.objects.all().delete()
    Job.objects.all().delete()

    print("Creating Demo Users...")
    # 1. Admin / Recruiter 1
    admin_user, _ = User.objects.get_or_create(username="admin", email="admin@smartjob.com")
    admin_user.set_password("admin123")
    admin_user.is_staff = True
    admin_user.is_superuser = True
    admin_user.save()

    recruiter1, _ = User.objects.get_or_create(username="recruiter_techcorp", email="hr@techcorp.io")
    recruiter1.set_password("recruiter123")
    recruiter1.save()
    RecruiterProfile.objects.update_or_create(user=recruiter1, defaults={"company_name": "TechCorp Innovations"})

    recruiter2, _ = User.objects.get_or_create(username="recruiter_fincloud", email="careers@fincloud.ai")
    recruiter2.set_password("recruiter123")
    recruiter2.save()
    RecruiterProfile.objects.update_or_create(user=recruiter2, defaults={"company_name": "FinCloud AI"})

    # 2. Candidates
    candidate1, _ = User.objects.get_or_create(username="candidate_alex", email="alex.dev@gmail.com")
    candidate1.set_password("candidate123")
    candidate1.save()

    candidate2, _ = User.objects.get_or_create(username="candidate_sarah", email="sarah.code@gmail.com")
    candidate2.set_password("candidate123")
    candidate2.save()

    print("Creating Demo Jobs...")
    job1 = Job.objects.create(
        recruiter=recruiter1,
        title="Python Full-Stack Developer",
        company="TechCorp Innovations",
        location="Bangalore / Hybrid",
        salary="₹12 - ₹18 LPA",
        experience="2 - 4 years",
        skills="Python, Django, React.js, PostgreSQL, Docker, REST APIs",
        description=(
            "We are looking for a skilled Python Full-Stack Developer to design and develop scalable web applications.\n\n"
            "Responsibilities:\n"
            "- Build robust RESTful APIs using Django / Django REST Framework.\n"
            "- Integrate dynamic frontend user interfaces with React.\n"
            "- Optimize PostgreSQL queries and cache hot data with Redis.\n"
            "- Write clean, maintainable unit and integration tests.\n\n"
            "Requirements:\n"
            "- Strong command of Python and object-oriented programming.\n"
            "- Solid experience with relational databases and ORMs.\n"
            "- Familiarity with Git, CI/CD pipelines, and cloud deployment."
        ),
    )

    job2 = Job.objects.create(
        recruiter=recruiter1,
        title="Backend Software Engineer (Python/FastAPI)",
        company="TechCorp Innovations",
        location="Remote (India)",
        salary="₹10 - ₹15 LPA",
        experience="1 - 3 years",
        skills="Python, FastAPI, Celery, Redis, Microservices",
        description=(
            "Join our core platform engineering team to build high-throughput async microservices.\n\n"
            "Key tasks include developing asynchronous background workers with Celery, "
            "optimizing database queries, and designing OpenAPI contracts."
        ),
    )

    job3 = Job.objects.create(
        recruiter=recruiter2,
        title="Senior Python / Django Architect",
        company="FinCloud AI",
        location="Hyderabad / Remote",
        salary="₹22 - ₹30 LPA",
        experience="5+ years",
        skills="Python, Django, AWS, Kubernetes, Distributed Systems",
        description=(
            "Lead the technical architecture for our next-generation automated fintech platforms. "
            "Drive code reviews, define security standards, and mentor mid-level developers."
        ),
    )

    job4 = Job.objects.create(
        recruiter=recruiter2,
        title="Junior Python Developer",
        company="FinCloud AI",
        location="Chennai",
        salary="₹5 - ₹8 LPA",
        experience="0 - 2 years",
        skills="Python, Django, HTML, CSS, JavaScript, SQLite",
        description=(
            "Great opportunity for early-career developers looking to sharpen their full-stack skills. "
            "You will work closely with senior mentors on feature development, bug fixes, and test automation."
        ),
    )

    print("Creating Demo Applications...")
    Application.objects.create(
        user=candidate1,
        job=job1,
        name="Alex Mercer",
        email="alex.dev@gmail.com",
        phone="+91 9876543210",
        skills="Python, Django, React, PostgreSQL",
        cover_letter="I have 2.5 years of experience building scalable Django REST backends and modern React frontends. Excited to contribute to TechCorp!",
        status="Under Review",
    )

    Application.objects.create(
        user=candidate2,
        job=job1,
        name="Sarah Jenkins",
        email="sarah.code@gmail.com",
        phone="+91 9123456789",
        skills="Python, FastAPI, Django, Docker",
        cover_letter="Passionate about writing clean Python code, testing, and database optimization. Looking forward to discussing this opportunity.",
        status="Selected",
    )

    Application.objects.create(
        user=candidate1,
        job=job2,
        name="Alex Mercer",
        email="alex.dev@gmail.com",
        phone="+91 9876543210",
        skills="Python, FastAPI, Redis, Microservices",
        cover_letter="Have worked with async Python and message queues on multiple production projects.",
        status="Pending",
    )

    print("Data seeded successfully!")
    print("\nAvailable Demo Credentials:")
    print("----------------------------------------------------------------")
    print("1. Recruiter Account:  username: recruiter_techcorp | password: recruiter123")
    print("2. Recruiter Account:  username: recruiter_fincloud | password: recruiter123")
    print("3. Candidate Account:  username: candidate_alex     | password: candidate123")
    print("4. Candidate Account:  username: candidate_sarah    | password: candidate123")
    print("5. Superuser/Admin:    username: admin              | password: admin123")
    print("----------------------------------------------------------------")


if __name__ == "__main__":
    seed_data()
