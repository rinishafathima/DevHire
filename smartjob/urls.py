from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static

from jobs import api_views as job_api_views
from applications import api_views as app_api_views

urlpatterns = [
    path("admin/", admin.site.urls),
    path("", include("accounts.urls")),
    path("jobs/", include("jobs.urls")),
    path("apply/", include("applications.urls")),

    # REST API Endpoints for Full-Stack / Mobile / Frontend integration
    path("api/jobs/", job_api_views.JobListCreateAPIView.as_view(), name="api_job_list"),
    path("api/jobs/<int:pk>/", job_api_views.JobDetailAPIView.as_view(), name="api_job_detail"),
    path("api/applications/", app_api_views.ApplicationListCreateAPIView.as_view(), name="api_application_list"),
    path("api/applications/<int:pk>/", app_api_views.ApplicationDetailAPIView.as_view(), name="api_application_detail"),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
