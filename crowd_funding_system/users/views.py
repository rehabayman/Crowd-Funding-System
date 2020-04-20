from django.shortcuts import render
from .models import User
from projects.models import Project
from django.http import HttpResponse

# Create your views here.
def show(request, id):
    user = User.objects.filter(id=id)[0]
    context = {"user": user}
    return render(request, "users/show.html", context)

def show_projects(request, id):
    user = User.objects.filter(id=id)[0]
    user_projects = user.project_set.all()
    context = {"user": user, "user_projects": user_projects}
    # return HttpResponse(f"{user_projects}")
    return render(request, "users/show_projects.html", context)
