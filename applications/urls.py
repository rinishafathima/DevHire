from django.urls import path
from . import views

urlpatterns = [
    path("<int:job_id>/", views.apply_job, name="apply_job"),
    path("application/<int:application_id>/status/", views.update_application_status, name="update_application_status"),
    path("application/<int:application_id>/offer-response/", views.respond_to_offer, name="respond_to_offer"),
]
