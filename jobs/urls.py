from django.urls import path
from . import views

urlpatterns = [
    path("", views.job_list, name="job_list"),
    path("details/<int:job_id>/", views.job_detail, name="job_detail"),
    path("add/", views.add_job, name="add_job"),
]