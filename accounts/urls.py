from django.urls import path
from . import views

urlpatterns = [
path("", views.home, name="home"),
path("register/", views.register, name="register"),
path("login/", views.user_login, name="login"),
path("dashboard/", views.dashboard, name="dashboard"),
path(
"recruiter-dashboard/",
views.recruiter_dashboard,
name="recruiter_dashboard"
),
path("logout/", views.user_logout, name="logout"),
]
