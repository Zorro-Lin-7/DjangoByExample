from django import forms


class LoginForm(forms.Form):
    username = form.CharField()
    password = forms.CharField(widget=forms.PasswordInput)
