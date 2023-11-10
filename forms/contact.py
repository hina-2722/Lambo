from django import forms

class ContactForm(forms.Form):
    user = forms.CharField(max_length=100,label ="保護者様")
    name =(forms.CharField(max_length=100,label ="お子様"))
    title = forms.CharField(max_length=50,label ="件名",widget=forms.TextInput(attrs={'placeholder': '件名を入力してください'}))
    message = forms.CharField(widget=forms.Textarea(attrs={'rows': 6, 'cols': 30}),label ="内容")
