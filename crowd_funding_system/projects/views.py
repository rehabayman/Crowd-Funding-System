from django.shortcuts import render, redirect
from django.http import JsonResponse
from .models import *
from .forms import new_project_form, ReportForm
from django.contrib.auth.decorators import login_required
# Create your views here.

@login_required
def index(request):
    projects = {"projects": Project.objects.all()}
    return render(request,"projects/index.html",projects)

@login_required
def project_details(request,project_id):
    target_project = Project.objects.get(id=project_id)
    if request.method.lower() == 'get':
        similar_projects = Project.objects.filter(category = target_project.category).exclude(id = target_project.id)[:4]
        project = {"project": target_project,"similar_projects": similar_projects}
        return render(request,"projects/project_details.html",project)
    elif request.method.lower() == 'delete':
        return render(request,"projects/index.html",projects)


def new_project(request):
    form = new_project_form(request.POST or None)
    if form.is_valid():
        form.save()
    
    context = {
        'form' : form
    }
    return render (request, "projects/new_project.html", context)

def check_before_report(project_id,user_id):
    if Project_Reports.objects.filter(project_id=project_id,user_id=user_id):
        return False
    else:
        return True

@login_required
def report_project(request,project_id):  
    if request.method.upper() == 'POST': 
        form = ReportForm(request.POST) 
        if form.is_valid(): 
            form = form.save(commit=False)
            form.project_id = project_id
            form.user_id = request.user.id
            if check_before_report(form.project_id,form.user_id):
                form.save()
                return redirect('project_details', project_id)
            else:
                response = JsonResponse({"error": "Sorry you have already reported this project !"})
                response.status_code = 403
                return response
    elif request.method.upper() == 'GET':
        form = ReportForm() 
        return render(request, 'projects/report_project.html', {'form' : form})