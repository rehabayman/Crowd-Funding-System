from django.contrib import admin
from .models import Project_Reports,Comment_Reports

# Register your models here.
@admin.register(Project_Reports)
class Project_Reports_Admin(admin.ModelAdmin):
    list_display = (
        'report_id',
        'user',
        'project',
        'report',
        'project_actions',
    )
    readonly_fields = (
        'report_id',
        'user',
        'project',
        'report',
        'project_actions',
    )