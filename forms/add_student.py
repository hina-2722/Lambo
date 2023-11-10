from django import forms
from Student.models import Student

class StudentForm(forms.ModelForm):
    class Meta:
        model = Student
        fields = ['student_name', 'first_name', 'last_name', 'gender', 'birth_date', 'grade', 'classroom']
        widgets = {
            'birth_date': forms.DateInput(attrs={'type': 'date'}),
        }
