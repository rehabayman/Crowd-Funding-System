from django.shortcuts import render
from projects.models import Project

def homepage_index(request):
    highest_rated_projects = sorted(Project.objects.all(), key=lambda a:a.average_rating, reverse=True)[:5]
    latest_projects = Project.objects.all().order_by('-created_at')[:5]
    featured_projects = Project.objects.filter(is_featured=True).order_by('-created_at')[:5]
    context = {
        "highest_rated_projects":highest_rated_projects,
        "latest_projects": latest_projects,
        "featured_projects": featured_projects
    }
    return render(request, "crowd_funding_system/homepage.html", context)