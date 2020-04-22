from django.shortcuts import render, get_object_or_404
from django.views.generic.edit import UpdateView, DeleteView
from django.http import HttpResponse, Http404, HttpResponseRedirect
from django.urls import reverse_lazy, reverse
from .forms import UserModelForm
from django.shortcuts import render,redirect
from users.models import User
from .models import User
from projects.models import Project
from django.core.exceptions import PermissionDenied
from django.contrib.auth.mixins import LoginRequiredMixin


class ProfileUpdate(LoginRequiredMixin,UpdateView):
    form_class= UserModelForm    
    template_name = 'users/_edit_profile.html'

    def get_object(self):
        id_=self.kwargs.get("id")
        user=User.objects.get(id__exact= id_)         
        if self.request.user == user:       
            return get_object_or_404(User,id=id_)
        raise PermissionDenied()

    def post(self, request,**kwargs):
        user= User.objects.get(id__exact=kwargs['id']) 
        profile_pic1= user.profile_pic
        form= UserModelForm(request.POST, request.FILES)

        if not request.FILES:           
            form.instance.profile_pic= user.profile_pic

        if request.user != user:
            return render(request,"home.html")

        if form.is_valid(): 
            form.instance.id = self.kwargs['id']
            form.save()                 
            context = {"form":form, "message": "You have Updated your Profile successfully"}
            return render(request,self.template_name,context)      
        
        context = {"form":form}
        return render(request,self.template_name, context)      
        

    def form_valid(self, form):
        return super().form_valid(form) 


class UserDelete(LoginRequiredMixin, DeleteView):
    model = User
    def get_object(self):        
        id_=self.kwargs.get("id")
        user=User.objects.get(id__exact= id_) 

        # if self.request.user == user:       
        return get_object_or_404(User,id=id_)
        raise PermissionDenied()

    def delete(self, request, *args, **kwargs):
        self.object = self.get_object()  

        if self.object == request.user:           
                self.object.delete()
                return HttpResponseRedirect(self.get_success_url())           
        else:            
            raise PermissionDenied()    
        
    success_url = '/' 


    # will reverse to login page
    # def get_success_url(self):
    #     return reverse.(crowd:login) 



# to test reverse in model
def test_home(request):
    return render(request,"home.html")



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
