from django import forms
from Reservation.models import Report

class ReportForm(forms.ModelForm):

    class Meta:
        model = Report
        fields = ['goal', 'achievement', 'comment']
        widgets = {
            'comment': forms.Textarea(attrs={'rows': 5, 'cols': 25}),
        }