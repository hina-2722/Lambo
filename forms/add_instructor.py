from django import forms
from Instructor.models import Instructor

class InstructorRegistrationForm(forms.Form):
    genders = (
    ('男', '男'),
    ('女', '女'),
)
    name = forms.CharField(max_length=100,label ="講師名")
    gender = forms.ChoiceField(label ="性別",choices=genders)
    birth_date = forms.DateField(label="生年月日",widget=forms.TextInput(attrs={'placeholder': '2023-05-09の型式'}))