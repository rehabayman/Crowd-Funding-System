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
import uuid

from django.core.files.storage import FileSystemStorage
from django.core.mail import send_mail
from django.utils import timezone
from django.contrib import messages

# Create your views here.



def register_user(request):
    context = {}
    user_creation_form = RegisterForm()
    if( request.method == "POST"):
        uploaded_image = request.FILES["profile_pic"]
        user_creation_form = RegisterForm(request.POST, request.FILES)
        if(user_creation_form.is_valid()):
            user = user_creation_form.save(commit=False)
            user.is_active = False
            
            user.set_expiration_date()
            user.set_activation_token()
            email = user.email
            token = user.get_activation_token()
            
            url_to_activate = "/users/activate/" + token + "/" + str(user.id)
            message = "Please activate your email with the next url "  + url_to_activate
            send_mail(
                'Account activation mail',
                message,
                'crowdFunding@example.com',
                [email],
                fail_silently=False,
            )
            user.save()
            fs = FileSystemStorage()
            fs.save(uploaded_image.name, uploaded_image)
            context['message'] = "Registered succcessfully, please wait for activation mail to use your account."
            context["form"] = user_creation_form
            return render(request, "register.html", context )


    context = { "form": user_creation_form }
    return render(request, "register.html", context )

    
def activate_user(request, active, user_id):
    context = {}
    user = User.objects.filter(activation_token=active, id=user_id)
    now = timezone.now()
    if user:
        user = user[0]
        if user.expiration_date > now:
            user.is_active = True
            user.save()
            messages.success(request, "Account has been activated successfully" )
            return redirect("/users/login")
        else:
            messages.success(request, "Sorry you didn't activate yor account, create another one?." )
            return redirect("/users/register", context)
    else: 
        messages.success(request, "Couldn't find your account, create one?." )
        return redirect("/users/register")

def login_user(request):
    context = {}
    if request.method == 'POST':

        username = request.POST.get("username")
        password = request.POST.get("password")
        if( username != "" and len(password) >= 8 ):
            user = authenticate(username=username, password=password)
            if user:
                if user.is_active:
                    login( request, user)
                    context["message"] = "Logged in successfully"
                    return render(request, "login.html", context)
                else:
                    context["message"] = "Your account is not activated yet"
                    return render(request, "login.html", context)
            else:
                context["message"] = "Couldn't find or wrong credentials."
                return render(request, "login.html", context)

        elif(password < 8 ):
            context["message"] = "password is less than 8 characters."
            return render(request, "login.html", context)
    return render(request, "login.html", context)



def logout_user(request):
    context = {}
    logout(request)
    return render(request, "home.html", context)

class ProfileUpdate(LoginRequiredMixin,UpdateView):
    form_class= UserModelForm    
    template_name = 'users/_edit_profile.html'
    
    def get_object(self):
        return get_object_or_404(User,id=self.request.user.id)
            

    def form_valid(self, form):       
        form.save()
        context = {"form":form, "message": "You have Updated your Profile successfully"}
        return render(self.request,self.template_name, context)
        
    success_url='/'

class UserDelete(LoginRequiredMixin, DeleteView):
    model = User
    def get_object(self):           
        return get_object_or_404(User,id=self.request.user.id)

    def delete(self, request, *args, **kwargs):
        self.object = self.get_object()        
        self.object.delete()
        return HttpResponseRedirect(self.get_success_url())                
    success_url = '/users/register' 


    # # will reverse to login page
    # def get_success_url(self):
    #     return reverse.(crowd:login) 



# to test reverse in model
def test_home(request):
    return render(request,"home.html")


@login_required
def show(request, id):
    if uuid.UUID(id) == request.user.id:
        user = request.user
        context = {"user": user}
        return render(request, "users/show.html", context)
    else:
        raise PermissionDenied()

@login_required
def show_projects(request, id):
    if uuid.UUID(id) == request.user.id:
        user = request.user
        user_projects = user.project_set.all()
        context = {"user": user, "user_projects": user_projects}
        return render(request, "users/show_projects.html", context)
    else:
        raise PermissionDenied()

@login_required
def show_donations(request, id):
    if uuid.UUID(id) == request.user.id:
        user = request.user
        user_donations = user.user_donations_set.all()
        context = {"user": user, "user_donations": user_donations}
        return render(request, "users/show_donations.html", context)
    else:
        raise PermissionDenied()
