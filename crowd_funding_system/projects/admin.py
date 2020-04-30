from django.contrib import admin
from .models import Project_Reports,Comment_Reports, Project, Category

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

@admin.register(Comment_Reports)
class Comment_Reports_Admin(admin.ModelAdmin):
    list_display = (
        'report_id',
        'user',
        'comment_content',
        'report',
        'comment_actions',
    )
    readonly_fields = (
        'report_id',
        'user',
        'comment_content',
        'report',
        'comment_actions',
    )

# admin.site.register(Project)
@admin.register(Project)
class Project_Admin(admin.ModelAdmin):
    list_display = (
        'title',
        'total_target',
        'created_at',
        'creator',
        'is_featured'
    )
    readonly_fields = (
        'id',
        'title',
        'details',
        'total_target',
        'start_date',
        'end_date',
        'created_at',
        'creator',
        'category'
    )

@admin.register(Category)
class Category_Admin(admin.ModelAdmin):
    list_display = (
        'category_name',
    )
    readonly_fields = (
        'id',
    )