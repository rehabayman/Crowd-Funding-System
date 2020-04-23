from django import forms
from django.forms import ModelForm

from .models import Project,Project_Reports

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