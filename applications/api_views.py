from rest_framework import generics, permissions
from .models import Application
from .serializers import ApplicationSerializer


class ApplicationListCreateAPIView(generics.ListCreateAPIView):
    """
    API endpoint for authenticated candidates to view their applications or submit a new application.
    """
    serializer_class = ApplicationSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        return Application.objects.filter(user=self.request.user).select_related("job").order_by("-applied_at")

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)


class ApplicationDetailAPIView(generics.RetrieveAPIView):
    """
    API endpoint to retrieve details of a specific application.
    """
    serializer_class = ApplicationSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        user = self.request.user
        if hasattr(user, "recruiterprofile"):
            return Application.objects.filter(job__recruiter=user)
        return Application.objects.filter(user=user)
