from django import forms
from django.contrib.auth.models import User


class SignupForm(forms.ModelForm):
    username = forms.CharField(label="Username", max_length=100)
    password1 = forms.CharField(label="Password", widget=forms.PasswordInput)
    password2 = forms.CharField(label="Confirm Password", widget=forms.PasswordInput)
    email = forms.CharField(label="Email")

    class Meta:
        model = User
        fields = ('username','email',)
