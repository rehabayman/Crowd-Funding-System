from django.shortcuts import render, get_object_or_404
from django.views.generic.edit import CreateView, DeleteView
from django.http import HttpResponse,HttpResponseRedirect, Http404
from django.urls import reverse_lazy, reverse
from .forms import UserDonationsModelForm
from .models import User_Donations, User 
from projects.models import Project
from django.core.validators import ValidationError
from django.db.models import Sum 
import decimal
from django import forms
from django.core.exceptions import PermissionDenied
from django.contrib.auth.mixins import LoginRequiredMixin
from .models import *
from .forms import new_project_form
from django.contrib.auth.decorators import login_required

def get_total_donations(id):
    if User_Donations.objects.filter(project_id=id).aggregate(total=Sum('amount'))['total']:
        total = decimal.Decimal(User_Donations.objects.filter(project_id=id).aggregate(total=Sum('amount'))['total'])
    else:
        total=0
    return total


class ProjectDonate(LoginRequiredMixin,CreateView):

    form_class= UserDonationsModelForm    
    template_name = 'projects/donate.html'  
    # login_url = '/login/'
    # redirect_field_name = 'redirect_to'
        
    def get_context_data(self, *args, **kwargs):          
        context = super(ProjectDonate, self).get_context_data(*args, **kwargs)
        total = get_total_donations(self.kwargs['id'])        
        p= Project.objects.get(id__exact=self.kwargs['id'])  
        
        if total >= p.total_target:
            context={"Done": "True", "message": "Project reached the target"}

        context["total"] = total
        return context
            

    def post(self, request,id):           
        total = get_total_donations(id)
        form=UserDonationsModelForm(request.POST)
        p= Project.objects.get(id__exact=id) 

        if form.is_valid():

            if  p.total_target < decimal.Decimal(request.POST['amount']) + total : 
                context = {"form":form, "error":"Donations Exceeded Total Target"}
                return render(request,self.template_name,context)

            form.instance.project_id = self.kwargs['id']
            form.instance.user_id= self.request.user
            form.save()
            form=UserDonationsModelForm()
            total = get_total_donations(id)
            context = {"form":form, "message": "You have Donated successfully", "total":total}
            return render(request,self.template_name,context)      
        
        context = {"form":form, "total":total}
        return render(request,self.template_name, context)   


class ProjectDelete(LoginRequiredMixin,DeleteView):
    model = Project
    template_name='projects/project_confirm_delete.html'  
    # login_url = '/login/'
    # redirect_field_name = 'redirect_to'
    
    def get_object(self):       

        id_=self.kwargs.get("id")      
        project=Project.objects.get(id__exact= id_)        
        total= get_total_donations(self.kwargs.get("id"))

        if project.creator == self.request.user:
            return get_object_or_404(Project,id=id_)  
        context = {"cant":"True"}        
        return context
        
    def delete(self, request, *args, **kwargs):
        self.object = self.get_object()
        user=User.objects.get(id__exact= "237450c29a95421eb5d06e60cdf7937b") 
        total= get_total_donations(self.kwargs.get("id"))       
        if self.object.creator == user:           
            if decimal.Decimal(total) < decimal.Decimal(self.object.total_target) * decimal.Decimal(0.25):  
                self.object.delete()
                return HttpResponseRedirect(self.get_success_url())
            else:
                return render(request,self.template_name,{"message":"Failed. Donations are more than 25% of project target", "object":self.object})  
        else:            
            raise PermissionDenied()
    success_url = '/' 

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
