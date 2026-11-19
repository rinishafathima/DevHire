from rest_framework import generics, permissions
from .models import Job
from .serializers import JobSerializer


class JobListCreateAPIView(generics.ListCreateAPIView):
    """
    API endpoint to list all jobs (with search/filtering) or post a new job.
    """
    serializer_class = JobSerializer

    def get_queryset(self):
        queryset = Job.objects.all().order_by("-id")
        search = self.request.query_params.get("search")
        location = self.request.query_params.get("location")

        if search:
            queryset = queryset.filter(title__icontains=search) | queryset.filter(skills__icontains=search)

        if location:
            queryset = queryset.filter(location__icontains=location)

        return queryset

    def perform_create(self, serializer):
        recruiter = self.request.user if self.request.user.is_authenticated else None
        serializer.save(recruiter=recruiter)


class JobDetailAPIView(generics.RetrieveUpdateDestroyAPIView):
    """
    API endpoint to retrieve, update, or delete a single job.
    """
    queryset = Job.objects.all()
    serializer_class = JobSerializer
