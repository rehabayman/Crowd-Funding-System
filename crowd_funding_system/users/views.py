from django.shortcuts import render, get_object_or_404
from django.views.generic.edit import UpdateView, DeleteView
from django.http import HttpResponse, Http404, HttpResponseRedirect
from django.urls import reverse_lazy, reverse
from .forms import UserModelForm
from django.shortcuts import render,redirect
from users.models import User
from .models import User
from django.core.exceptions import PermissionDenied
from django.contrib.auth.mixins import LoginRequiredMixin
from projects.models import Project, User_Donations
from django.contrib.auth.decorators import login_required

from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.forms import UserCreationForm
from users.forms import RegisterForm, LoginForm
from django.http import HttpResponseRedirect, HttpResponse
from django.urls import reverse
from django.contrib.auth.decorators import login_required

from django.core.files.storage import FileSystemStorage

# Create your views here.


def register_user(request):
    context = {}
    user_creation_form = RegisterForm()

    if( request.method == "POST"):
        uploaded_image = request.FILES["profile_pic"]
        user_creation_form = RegisterForm(request.POST, request.FILES)
        if(user_creation_form.is_valid()):
            user_creation_form.save()
            fs = FileSystemStorage()
            fs.save(uploaded_image.name, uploaded_image)
            context['message'] = "registered succcessfully."
            context["form"] = user_creation_form
            return render(request, "register.html", context )


    context = { "form": user_creation_form }
    return render(request, "register.html", context )

    

def login_user(request):
    context = {}
    if request.method == 'POST':

        username = request.POST.get("username")
        password = request.POST.get("password")
        # form = LoginForm(request.POST)
        # print(form.is_valid())
        print(username)
        print(password)
        if( username != "" and len(password) >= 8 ):
            user = authenticate(username=username, password=password)
            if user:
                print("user is authenticated")
                if user.is_active:
                    login( request, user)
                    context["message"] = "Logged in successfully"
                    return render(request, "login.html", context)
                else:
                    context["message"] = "Your account is not activated yet"
                    return render(request, "login.html", context)
            else:
                print("user is not authenticated")
                print( user)
                context["message"] = "Couldn't find or wrong credentials."
                # context['form'] = LoginForm
                return render(request, "login.html", context)

        elif(password < 8 ):
            context["message"] = "password is less than 8 characters."
            return render(request, "login.html", context)
    # context['form'] = LoginForm
    return render(request, "login.html", context)



def logout_user(request):
    context = {}
    logout(request)
    return render(request, "home.html", context)

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


@login_required
def show(request, id):
    # if id == request.user.id:
    user = User.objects.filter(id=id)[0]
    context = {"user": user}
    return render(request, "users/show.html", context)
    # else:
        # raise PermissionDenied()

@login_required
def show_projects(request, id):
    # if id == request.user.id:
    user = User.objects.filter(id=id)[0]
    user_projects = user.project_set.all()
    context = {"user": user, "user_projects": user_projects}
    return render(request, "users/show_projects.html", context)
    # else:
        # raise PermissionDenied()

@login_required
def show_donations(request, id):
    # if id == request.user.id:
    user = User.objects.filter(id=id)[0]
    user_donations = user.user_donations_set.all()
    context = {"user": user, "user_donations": user_donations}
    return render(request, "users/show_donations.html", context)
    # else:
        # raise PermissionDenied()
