from django import forms
from dashboard.models import Workbook

class WorkbookForm(forms.ModelForm):
    class Meta:
        model = Workbook
        fields = ['name', 'price', 'image', 'purchase_link', 'level', 'student']
