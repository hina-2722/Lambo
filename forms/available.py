from django import forms
from django.forms.widgets import DateInput
from Instructor.models import Schedule, TimeSlot, Instructor
from django.shortcuts import get_object_or_404

class ScheduleForm(forms.ModelForm):
    time = forms.ModelMultipleChoiceField(
        queryset=TimeSlot.objects.all(),
        widget=forms.CheckboxSelectMultiple,
        required=True
    )
    instructor_name = forms.CharField(max_length=100, label="講師名")

    class Meta:
        model = Schedule
        fields = '__all__'
        widgets = {
            'date': DateInput(attrs={'type': 'date'}),
        }


    def clean_instructor_name(self):
        instructor_name = self.cleaned_data.get('instructor_name')
        instructor = get_object_or_404(Instructor, name=instructor_name)
        return instructor
    