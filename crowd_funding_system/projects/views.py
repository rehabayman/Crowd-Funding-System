from django.shortcuts import render, redirect, get_object_or_404
from .models import Project, Project_Ratings, User_Donations
from users.models import User
from .forms import AddProjectRatingForm, UserDonationsModelForm
from django.views.generic.edit import CreateView, DeleteView
from django.http import HttpResponse, HttpResponseRedirect, Http404
from django.urls import reverse_lazy, reverse
from django.core.validators import ValidationError
from django.db.models import Sum
import decimal
from django import forms
from django.core.exceptions import PermissionDenied
from django.contrib.auth.mixins import LoginRequiredMixin
from .models import *
from .forms import new_project_form
from django.contrib.auth.decorators import login_required
from .filters import ProjectFilter


def get_total_donations(id):
    if User_Donations.objects.filter(project_id=id).aggregate(total=Sum('amount'))['total']:
        total = decimal.Decimal(User_Donations.objects.filter(
            project_id=id).aggregate(total=Sum('amount'))['total'])
    else:
        total = 0
    return total


class ProjectDetails(CreateView):

    form_class = UserDonationsModelForm
    template_name = 'projects/project_details.html'
    # login_url = '/login/'
    # redirect_field_name = 'redirect_to'

    def get_context_data(self, *args, **kwargs):
        context = super(ProjectDetails, self).get_context_data(*args, **kwargs)
        total = get_total_donations(self.kwargs['id'])
        p = Project.objects.get(id__exact=self.kwargs['id'])

        if total >= p.total_target:
            context = {"Done": "True", "message": "Project reached the target"}

        context["total"] = total

        current_user = User.objects.all()[0]
        project_rating = Project.objects.filter(
            id=self.kwargs['id'], creator=current_user.id)[0].project_ratings_set.all()
        rating = 0
        if project_rating.count() != 0:
            rating = project_rating[0].rating
        target_project = Project.objects.get(id=self.kwargs['id'])
        similar_projects = Project.objects.filter(
            category=target_project.category).exclude(id=target_project.id)[:4]
        project = {"project": target_project,
                   "similar_projects": similar_projects}
        # return render(request,"projects/project_details.html",project)

        context["project"] = project
        context["rating"] = rating
        # return render(request,"projects/project_details.html",{"project": project, "rating": rating})
        return context

    def post(self, request, id):
        current_user = User.objects.all()[0]

        total = get_total_donations(id)
        form = UserDonationsModelForm(request.POST)
        p = Project.objects.get(id__exact=id)
        project_rating = Project.objects.filter(
            id=self.kwargs['id'], creator=current_user.id)[0].project_ratings_set.all()
        rating = 0
        if project_rating.count() != 0:
            rating = project_rating[0].rating
        target_project = Project.objects.get(id=self.kwargs['id'])
        similar_projects = Project.objects.filter(
            category=target_project.category).exclude(id=target_project.id)[:4]
        project = {"project": target_project,
                   "similar_projects": similar_projects}

        if form.is_valid():

            if p.total_target < decimal.Decimal(request.POST['amount']) + total:
                context = {
                    "form": form, "error": "Donations Exceeded Total Target", "total": total}
                context["project"] = project
                context["rating"] = rating
                return render(request, self.template_name, context)

            form.instance.project_id = self.kwargs['id']
            # form.instance.user_id= self.request.user
            form.instance.user_id = "45937d98d5434d7c9b83f5b208dabe86"
            form.save()
            form = UserDonationsModelForm()
            total = get_total_donations(id)

            # return render(request,"projects/project_details.html",project)

            context = {
                "form": form, "message": "You have Donated successfully", "total": total}
            context["project"] = project
            context["rating"] = rating
            return render(request, self.template_name, context)

        context = {"form": form, "total": total}
        context["project"] = project
        context["rating"] = rating
        return render(request, self.template_name, context)


class ProjectDelete(DeleteView):
    model = Project
    template_name = 'projects/project_confirm_delete.html'
    # login_url = '/login/'
    # redirect_field_name = 'redirect_to'

    def get_object(self):

        id_ = self.kwargs.get("id")
        project = Project.objects.get(id__exact=id_)
        total = get_total_donations(self.kwargs.get("id"))

        # if project.creator == self.request.user:
        return get_object_or_404(Project, id=id_)
        context = {"cant": "True"}
        return context

    def delete(self, request, *args, **kwargs):
        self.object = self.get_object()
        user = User.objects.get(id__exact="237450c29a95421eb5d06e60cdf7937b")
        total = get_total_donations(self.kwargs.get("id"))
        if self.object.creator == user:
            if decimal.Decimal(total) < decimal.Decimal(self.object.total_target) * decimal.Decimal(0.25):
                self.object.delete()
                return HttpResponseRedirect(self.get_success_url())
            else:
                return render(request, self.template_name, {"message": "Failed. Donations are more than 25% of project target", "object": self.object})
        else:
            raise PermissionDenied()
    success_url = '/'

# Create your views here.

# @login_required


def index(request):
    projects = Project.objects.all()
    myFilter = ProjectFilter(request.GET, queryset=projects)
    projects = myFilter.qs
    projects = {"projects": projects, "myFilter": myFilter}
    return render(request, "projects/index.html", projects)

# @login_required
# def project_details(request,project_id):
#     # This is for testing right now
#     current_user = User.objects.all()[0]
#     project_rating = Project.objects.filter(id=project_id, creator = current_user.id)[0].project_ratings_set.all()
#     rating = 0
#     if project_rating.count() != 0:
#         rating = project_rating[0].rating
#     target_project = Project.objects.get(id=project_id)
#     similar_projects = Project.objects.filter(category = target_project.category).exclude(id = target_project.id)[:4]
#     project = {"project": target_project,"similar_projects": similar_projects}
#     # return render(request,"projects/project_details.html",project)


#     return render(request,"projects/project_details.html",{"project": project, "rating": rating})

# @login_required
def new_project(request):
    form = new_project_form(request.POST or None)
    if form.is_valid():
        form.save()

    context = {
        'form': form
    }
    return render(request, "projects/new_project.html", context)


def edit_project_rating(request, id):
    # current_user = request.user
    # if request.user.is_authenticated:
    #     pass
    # else:
    #     pass
    current_user = User.objects.all()[0]
    project_rating = Project.objects.filter(id=id, creator=current_user.id)[0].project_ratings_set.all()
    project = Project.objects.filter(id=id)[0]
    if request.method == "GET":
        rating = 0
        if project_rating.count() != 0:
            rating = project_rating[0].rating
        return redirect('projects:project_details', id=id)

    elif request.method == "POST":
        rating_form = AddProjectRatingForm(request.POST)
        rating = 0
        if rating_form.is_valid():
            if project_rating.count() != 0:
                project_rating_obj = project_rating[0]
                project_rating_obj.rating = rating_form.cleaned_data['rating']
                project_rating_obj.save()
            else:
                new_rating = Project_Ratings(
                    rating=rating_form.cleaned_data['rating'], project=project, user=current_user)
                new_rating.save()
            rating = rating_form.cleaned_data['rating']
        return redirect('projects:project_details', id=id)
