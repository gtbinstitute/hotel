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

    def clean_password2(self):
        pass1 = self.cleaned_data.get("password1")
        pass2 = self.cleaned_data.get("password2")
        if pass1 and pass2 and pass1 != pass2:
            raise forms.ValidationError("Password does not match or not entered")
        return pass2

    def save(self, commit=True):
        userobj = super(SignupForm, self).save(commit=False)
        userobj.set_password(self.cleaned_data["password2"])
        # userobj.is_active = False
        if commit:
            userobj.save()
        return userobj