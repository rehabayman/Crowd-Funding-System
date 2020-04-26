from django.shortcuts import render, redirect, get_object_or_404
from users.models import User
from django.views.generic.edit import CreateView, DeleteView
from django.http import HttpResponse, HttpResponseRedirect, Http404, JsonResponse
from django.urls import reverse_lazy, reverse
from django.core.validators import ValidationError
from django.db.models import Sum
import decimal
from django import forms
from django.core.exceptions import PermissionDenied
from django.contrib.auth.mixins import LoginRequiredMixin
from .models import *
from .forms import *
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

        project_id= self.kwargs['id']  
        user= self.request.user      
        context = super(ProjectDetails, self).get_context_data(*args, **kwargs)
        total_donations = get_total_donations(project_id)
        p = Project.objects.get(id__exact=project_id)   
        comments = Comment.objects.filter(project=p.id)             

        if total_donations >= p.total_target:
            context = {"Done": "True", "message": "Project reached the target"}

        context["total"] = total_donations

        current_user = self.request.user
        project_rating = Project.objects.filter(
            id=project_id)[0].project_ratings_set.filter(user=current_user.id)
        rating = 0
        if project_rating.count() != 0:
            rating = project_rating[0].rating
        
        target_project = Project.objects.get(id=project_id)        
        similar_projects = Project.objects.filter(
            category=target_project.category).exclude(id=target_project.id)[:4]
        
        project = {"project": target_project,
                   "similar_projects": similar_projects}

        context["project"] = project
        context["rating"] = rating
        context['comments']= comments
        return context

    def post(self, request, id):
        current_user = request.user
        total = get_total_donations(id)
        ####### rating########
        project_rating = Project.objects.filter(
            id=self.kwargs['id'])[0].project_ratings_set.filter(user=current_user.id)
        rating = 0
        if project_rating.count() != 0:
            rating = project_rating[0].rating
        
        target_project = Project.objects.get(id=self.kwargs['id'])
        comments = Comment.objects.filter(project=target_project.id)
        similar_projects = Project.objects.filter(
            category=target_project.category).exclude(id=target_project.id)[:4]
        project = {"project": target_project,
                   "similar_projects": similar_projects}

        ###### Donations form #######
        form = UserDonationsModelForm(request.POST)
        if form.is_valid():

            if target_project.total_target < decimal.Decimal(request.POST['amount']) + total:
                context = {
                    "form": form, "error": "Donations Exceeded Total Target", "total": total}
                context["project"] = project
                context["rating"] = rating
                context["comments"]=comments
                return render(request, self.template_name, context)

            form.instance.project_id = self.kwargs['id']
            form.instance.user_id= self.request.user.id
            form.save()
            form = UserDonationsModelForm()
            
            total = get_total_donations(id)
            ## set context ####
            context = {
                "form": form, "message": "You have Donated successfully", "total": total}
            context["project"] = project
            context["rating"] = rating
            context['comments']=comments   
            return render(request, self.template_name, context)
        ## set context ####
        context = {"form": form, "total": total}
        context["project"] = project
        context["rating"] = rating
        context['comments']=comments   
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

        if project.creator == self.request.user:
            return get_object_or_404(Project, id=id_)
        context = {"cant": "True"}
        return context

    def delete(self, request, *args, **kwargs):
        self.object = self.get_object()        
        total = get_total_donations(self.kwargs.get("id"))
        if self.object.creator == request.user:
            if decimal.Decimal(total) < decimal.Decimal(self.object.total_target) * decimal.Decimal(0.25):
                self.object.delete()
                return HttpResponseRedirect(self.get_success_url())
            else:
                response = JsonResponse({"error": "Failed. Donations are more than 25% of project target"})
                response.status_code = 403
                return response
        else:
            raise PermissionDenied()
    success_url = '/projects'


# @login_required

@login_required
def index(request):
    context = {}
    context["projects"] = Project.objects.all()
    context["myFilter"] = ProjectFilter(request.GET, queryset=context["projects"])

    tag = request.GET.get("tag")
    if( tag ):
        context["projects"] = Project.objects.raw("Select * from projects_project, projects_project_tags WHERE projects_project_tags.tag = %s AND projects_project.id = projects_project_tags.project_id", [tag])
        print(context["projects"])   
    elif(request.GET.get("title")):
        myFilter = ProjectFilter(request.GET, queryset=context["projects"])
        context["projects"] = myFilter.qs
        # projects = {"projects": projects, "myFilter": myFilter} #, "TagFilter": projectTagged
    return render(request, "projects/index.html", context)

@login_required
def new_project(request):
    form = new_project_form(request.POST or None)
    if form.is_valid():
        #form.creator = request.user
        form.save()
        return redirect('/projects/')
    context = {
        'form': form
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
                response = JsonResponse({"success": "Project reported successfully"})
                response.status_code = 200
                return response
            else:
                response = JsonResponse({"error": "Sorry you have already reported this project !"})
                response.status_code = 403
                return response
    elif request.method.upper() == 'GET':
        form = ReportForm() 
        return render(request, 'projects/report_project.html', {'form' : form})


def edit_project_rating(request, id):
    current_user = request.user
    project = Project.objects.filter(id=id)[0]
    # if request.user.is_authenticated and current_user.id != project.creator_id:
        # pass
    # else:
    #     pass
    project_rating = Project.objects.filter(id=id)[0].project_ratings_set.filter(user=current_user.id)
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


####### Adding comment #########
# @login_required
def add_comment(request,project_id):
    target_project = Project.objects.get(id=project_id)
    commentform = comment_form(request.POST)

    if request.method == 'POST':
        if commentform.is_valid():
            comment = commentform.save(commit=False)
            comment.project = target_project            
            comment.user = request.user            
            comment.save()
            commentform = comment_form()
            redirect('projects:project_details', project_id)            
    else:
        commentform = comment_form()
    similar_projects = Project.objects.filter(category = target_project.category).exclude(id = target_project.id)[:4]
    return redirect('projects:project_details', id=project_id)

######## Adding reply on comment ###########
def add_reply_on_comment(request, project_id, comment_id):
    replyform = reply_form(request.POST)
    comment = Comment.objects.get(id=comment_id)
    if request.method == 'POST':
        if replyform.is_valid():
            reply = replyform.save(commit=False)
            reply.user = request.user
            reply.comment = comment
            reply.save()
            replyform = reply_form()
            redirect('projects:project_details', project_id)
        else:
            replyform = reply_form()
    return redirect('projects:project_details', id=project_id)