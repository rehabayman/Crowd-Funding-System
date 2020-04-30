from django import forms
from django.forms import ModelForm
from .models import *
import decimal
from functools import partial
from django.utils.translation import ugettext_lazy as _

class AddProjectRatingForm(forms.ModelForm):   
    class Meta:
        model = Project_Ratings
        fields = ('rating',)

class UserDonationsModelForm(forms.ModelForm):   

    class Meta:
        model=User_Donations
        fields = ['amount']
  
    def clean_amount(self):             
        amount = self.cleaned_data.get('amount')        
        if amount <= 0:
            raise forms.ValidationError("Amount is invalid")
        return amount
    
class comment_form(forms.ModelForm):
    class Meta:
        model = Comment
        fields = [
            'comment',
        ]

class DateInput(forms.DateInput):
    input_type = 'date'

class DecimalInput(forms.NumberInput):
    input_type = 'number'

class new_project_form(forms.ModelForm):
    class Meta:
        model = Project
        fields = [
            'title',
            'details',
            'total_target',
            'start_date',
            'end_date',
            'category'
        ]
        widgets = {
            'title': forms.TextInput(attrs={'class':'form-control', 'style':'width:500px'}),
            'details': forms.TextInput(attrs={'class':'form-control'}),
            'total_target': DecimalInput(attrs={'class':'form-control'}),
            'start_date': DateInput(attrs={'class':'form-control'}),
            'end_date': DateInput(attrs={'class':'form-control'}),
            }

class NewProjectPicturesForm(forms.ModelForm):
    picture = forms.ImageField(widget=forms.ClearableFileInput(attrs={'multiple': True}))
    class Meta:
        model=Project_Pictures
        fields = ['picture',]
        widgets = {'project': forms.HiddenInput()}

class NewProjectTagsForm(forms.ModelForm):
    class Meta:
        model=Project_Tags
        fields = ['tag',]
        labels = {
            'tag': _('Tags: *Comma Separated:')
        }
        widgets = {
            'project': forms.HiddenInput(),
            'tag': forms.TextInput(attrs={'class':'form-control', 'style':'width:500px'}),
        }

class ReportForm(ModelForm):
    class Meta:
        model = Project_Reports
        fields = ['report',]

class CommentReportForm(ModelForm):
    class Meta:
        model = Comment_Reports
        fields = ['report',]

class reply_form(ModelForm):
    class Meta:
        model = Comment_Replies
        fields = ['content']