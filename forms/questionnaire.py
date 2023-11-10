from django import forms
from dashboard.models import TeacherEvaluation

class TeacherEvaluationForm(forms.ModelForm):
    class Meta:
        model = TeacherEvaluation
        fields = ['instructor','instructor_rating', 'curriculum_rating', 'satisfaction_rating', 'comment']

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['instructor'].widget.attrs['class'] = 'form-select'