from django.shortcuts import render, get_object_or_404
from django.views.generic.edit import UpdateView, DeleteView
from django.http import HttpResponse
from django.urls import reverse_lazy, reverse
from .forms import UserModelForm
from django.shortcuts import render
from users.models import User
from .models import User
from projects.models import Project


class ProfileUpdate(UpdateView):
    form_class= UserModelForm    
    template_name = 'users/_edit_profile.html'

    def get_object(self):
        id_=self.kwargs.get("id")
        return get_object_or_404(User,id=id_)

    def form_valid(self, form):
        return super().form_valid(form) 


class UserDelete(DeleteView):
    model = User
    def get_object(self):
        id_=self.kwargs.get("id")
        return get_object_or_404(User,id=id_)
        
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
