from django import forms
from User.models import User
from django.contrib.auth.password_validation import validate_password
import random

class SignupForm(forms.ModelForm):
     username = forms.CharField(label='保護者名')
     email = forms.EmailField(label='メールアドレス')
     password = forms.CharField(label='パスワード', widget=forms.PasswordInput())
     def clean_email(self):
        email = self.cleaned_data.get('email')
        if User.objects.filter(email=email).exists():
            raise forms.ValidationError('このメールアドレスは既に登録されています。')
        return email

     def clean(self):
        cleaned_data = super().clean()
        while True:
            customer_id = str(random.randint(100000, 999999))
            if not User.objects.filter(customer_id=customer_id).exists():
                break
        cleaned_data['customer_id'] = customer_id
        return cleaned_data

     class Meta:
        model = User
        fields = ['username', 'email', 'password']
     
     def save(self, commit=False):
       user = super().save(commit=False)
       validate_password(self.cleaned_data['password'], user)
       user.set_password(self.cleaned_data['password'])
       user.save()
       return user