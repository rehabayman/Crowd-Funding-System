from django.shortcuts import render
from .forms import new_project_form
from .models import Project

def new_project(request):
    form = new_project_form(request.POST or None)
    if form.is_valid():
        form.save()
    
    context = {
        'form' : form
    }
    return render (request, "projects/new_project.html", context)