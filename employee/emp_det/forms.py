from django import forms
from .models import Employee, Project
import re

class EmployeeForm(forms.ModelForm):
    class Meta:
        model = Employee
        fields = ['name', 'phone', 'company', 'role', 'active', 'state', 'address']
    
    def clean_phone(self):
        phone = self.cleaned_data.get('phone', [])
        if not isinstance(phone, list):
            raise forms.ValidationError("Phone numbers must be a list.")
        
        errors = []
        for phone in phone:
            if not re.match(r'^\d{10}$', phone):
                errors.append(f"Invalid phone number: {phone}. Each phone number must be exactly 10 digits.")
        
        if errors:
            raise forms.ValidationError(errors)
        
        return phone


class ProjectForm(forms.ModelForm):
    class Meta:
        model = Project
        fields = ['title', 'description', 'start_date', 'end_date', 'status']
