from django.shortcuts import render
from .models import *
from django.contrib.auth.decorators import login_required
# Create your views here.

@login_required
def index(request):
    projects = {"projects": Project.objects.all()}
    return render(request,"projects/index.html",projects)
@login_required
def project_details(request,project_id):
    target_project = Project.objects.get(id=project_id)
    similar_projects = Project.objects.filter(category_id = target_project.category_id).exclude(id = target_project.id)[:4]
    project = {"project": target_project,"similar_projects": similar_projects}
    return render(request,"projects/project_details.html",project)