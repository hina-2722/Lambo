from django import forms
from Student.models import Absence


class AbsenceForm(forms.ModelForm):
    class Meta:
        model = Absence
        fields = ['date', 'reason']