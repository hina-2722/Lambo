from django import forms
from django.contrib.auth.forms import AuthenticationForm

class LoginForm(AuthenticationForm):  # 追加
   username = forms.CharField(label='ID', max_length=6)
   password = forms.CharField(label='パスワード', widget=forms.PasswordInput)