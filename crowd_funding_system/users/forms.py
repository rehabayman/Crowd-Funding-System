from django import forms
from .models import User
class UserModelForm(forms.ModelForm):   
    class Meta:
        model=User
        exclude=['email']
    def __init__(self, *args, **kwargs):
        super(UserModelForm, self).__init__(*args, **kwargs)
        self.fields['profile_pic'].required = False   