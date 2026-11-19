
from django.contrib import admin
from .models import Application


@admin.register(Application)
class ApplicationAdmin(admin.ModelAdmin):

    list_display = (
        "id",
        "name",
        "job",
        "email",
        "status",
        "applied_at",
    )

    list_filter = (
        "status",
        "job",
        "applied_at",
    )

    search_fields = (
        "name",
        "email",
        "job__title",
    )

