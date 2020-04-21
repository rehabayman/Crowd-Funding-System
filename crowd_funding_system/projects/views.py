from django.shortcuts import render
from .models import *
from .forms import new_project_form
from django.contrib.auth.decorators import login_required
# Create your views here.

@login_required
def index(request):
    projects = {"projects": Project.objects.all()}
    return render(request,"projects/index.html",projects)

@login_required
def project_details(request,project_id):
    target_project = Project.objects.get(id=project_id)
    similar_projects = Project.objects.filter(category = target_project.category).exclude(id = target_project.id)[:4]
    project = {"project": target_project,"similar_projects": similar_projects}
    return render(request,"projects/project_details.html",project)

def new_project(request):
    form = new_project_form(request.POST or None)
    if form.is_valid():
        form.save()
    
    context = {
        'form' : form
    }
    return render (request, "projects/new_project.html", context)
