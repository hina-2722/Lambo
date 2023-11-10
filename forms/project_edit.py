from django import forms
from Student.models import Project

class ProjectForm(forms.ModelForm):
    class Meta:
        model = Project
        fields = ["name", 'description', 'start_date', 'end_date', 'members']
        widgets = {
            'members': forms.CheckboxSelectMultiple
        }