from django import forms
from .models import User_Donations, Project
import decimal

class UserDonationsModelForm(forms.ModelForm):   

    class Meta:
        model=User_Donations
        fields = ['amount']
  
    def clean_amount(self):             
        amount = self.cleaned_data.get('amount')        
        if amount <= 0:
            raise forms.ValidationError("Amount is invalid")
        return amount
    


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
