from django.shortcuts import render, redirect
from .models import Project, Project_Ratings
from users.models import User
from .forms import AddProjectRatingForm
from django.http import HttpResponse
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
    # This is for testing right now
    current_user = User.objects.all()[0]
    project_rating = Project.objects.filter(id=project_id, creator = current_user.id)[0].project_ratings_set.all()
    rating = 0
    if project_rating.count() != 0:
        rating = project_rating[0].rating
    target_project = Project.objects.get(id=project_id)
    similar_projects = Project.objects.filter(category = target_project.category).exclude(id = target_project.id)[:4]
    project = {"project": target_project,"similar_projects": similar_projects}
    return render(request,"projects/project_details.html",{"project": project, "rating": rating})

def new_project(request):
    form = new_project_form(request.POST or None)
    if form.is_valid():
        form.save()
    
    context = {
        'form' : form
    }
    return render (request, "projects/new_project.html", context)


def edit_project_rating(request, id):
    # current_user = request.user
    # if request.user.is_authenticated:
    #     pass
    # else:
    #     pass
    current_user = User.objects.all()[0]
    project_rating = Project.objects.filter(id=id, creator = current_user.id)[0].project_ratings_set.all()
    project = Project.objects.filter(id=id)[0]
    if request.method == "GET":
        rating = 0
        # rating_form = AddProjectRatingForm()
        if project_rating.count() != 0:
            rating = project_rating[0].rating
            # rating_form = AddProjectRatingForm(initial={'rating': project_rating[0].rating})
            # rating_form = AddProjectRatingForm(project_rating[0])
        # return render(request, "projects/project_details.html", {"project": project, "rating": rating})
        return redirect('project_details', project_id=id)
        

    elif request.method == "POST":
        rating_form = AddProjectRatingForm(request.POST)
        rating = 0
        if rating_form.is_valid():
            if project_rating.count() != 0:
                project_rating_obj = project_rating[0]
                project_rating_obj.rating = rating_form.cleaned_data['rating']       
                project_rating_obj.save()
            else:
                new_rating = Project_Ratings(rating=rating_form.cleaned_data['rating'], project=project, user=current_user)
                new_rating.save()
            rating = rating_form.cleaned_data['rating']
        # return render(request, "projects/project_details.html", {"project": project, "rating": rating})
        return redirect('project_details', project_id=id)
    