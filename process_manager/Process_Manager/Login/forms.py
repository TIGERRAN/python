from django import forms

class LoginForm(forms.Form):
    user = forms.CharField()
    password = forms.CharField()