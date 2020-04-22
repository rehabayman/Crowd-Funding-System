from django.shortcuts import render
from .models import Project, Project_Ratings
from users.models import User
from .forms import AddProjectRatingForm
from django.http import HttpResponse

# Create your views here.
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
        rating_form = AddProjectRatingForm()
        if project_rating.count() != 0:
            rating_form = AddProjectRatingForm(initial={'rating': project_rating[0].rating})
            # rating_form = AddProjectRatingForm(project_rating[0])
        return render(request, "projects/edit_rating.html", {"form": rating_form, "project": project})

    elif request.method == "POST":
        rating_form = AddProjectRatingForm(request.POST)
        if rating_form.is_valid():
            if project_rating.count() != 0:
                project_rating[0].rating = rating_form.cleaned_data['rating']       
                project_rating[0].save()
            else:
                new_rating = Project_Ratings(rating=rating_form.cleaned_data['rating'], project=project, user=current_user)
                new_rating.save()
        return render(request, "projects/edit_rating.html", {"form": rating_form, "project": project})
    
