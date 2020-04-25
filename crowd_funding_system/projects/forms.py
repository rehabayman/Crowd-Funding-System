from django import forms
from django.forms import ModelForm
from .models import Project, Project_Ratings, User_Donations, Project_Reports, Comment
import decimal

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


class new_project_form(forms.ModelForm):
    class Meta:
        model = Project
        fields = [
            'title',
            'details',
            'total_target',
            'start_date',
            'end_date',
            'creator',
            'category'
        ]

class ReportForm(ModelForm):
    class Meta:
        model = Project_Reports
        fields = ['report',]
