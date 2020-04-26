from django import forms
from .models import User

from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from users.models import User

from django.forms import ModelForm

class UserModelForm(forms.ModelForm):   
    class Meta:
        model=User
        exclude=['username','email','date_joined','is_active','is_superuser','is_staff','is_active','groups','user_permissions','password','last_login']
    def __init__(self, *args, **kwargs):
        super(UserModelForm, self).__init__(*args, **kwargs)
        self.fields['profile_pic'].required = False   


class RegisterForm(UserCreationForm):

    class Meta:
        model = User
        # password = forms.CharField(widget=forms.PasswordInput)
        fields = [ "username", "first_name", "last_name", "phone", "email", "profile_pic", "password1", "password2"]
        # widgets = {
        #     "password": forms.PasswordInput()
        # }
        


class LoginForm(AuthenticationForm):
    class Meta:
        model = User
        # fields = ["email", "password"]
        # widgets = {
        #     "password": forms.PasswordInput()
        # }
