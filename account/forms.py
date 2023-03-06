from django import forms
from django.core.validators import ValidationError
from django.contrib.auth.models import User


class RegisterForm(forms.Form):
    username = forms.CharField(max_length=35, widget=forms.TextInput(attrs={'placeholder': 'Your Username', 'class': 'form-control'}))
    email = forms.EmailField(widget=forms.EmailInput(attrs={'placeholder': 'Your Email', 'class': 'form-control'}))
    password1 = forms.CharField(min_length=8, max_length=50, widget=forms.PasswordInput(attrs={'placeholder': 'Your Password', 'class': 'form-control'}))
    password2 = forms.CharField(min_length=8, max_length=50, widget=forms.PasswordInput(attrs={'placeholder': 'Your Repeat password', 'class': 'form-control'}))

    def clean(self):
        cd = super().clean()
        p1 = cd.get('password1')
        p2 = cd.get('password2')

        if p1 and p2 and p1 != p2:
            raise ValidationError('password must match.')

    def clean_username(self):
        username = self.cleaned_data['username']
        user = User.objects.filter(username=username).exists()
        if user:
            raise ValidationError('this user by username already exists. ')
        return username

    def clean_email(self):
        email = self.cleaned_data['email']
        user = User.objects.filter(email=email).exists()
        if user:
            raise ValidationError('This email already exists the previous . ')
        return email


class LoginForm(forms.Form):
    username = forms.CharField(max_length=35, widget=forms.TextInput(attrs={'placeholder': 'Your Username', 'class': 'form-control'}))
    password = forms.CharField(max_length=50, widget=forms.PasswordInput(attrs={'placeholder': 'Your Password', 'class': 'form-control'}))


