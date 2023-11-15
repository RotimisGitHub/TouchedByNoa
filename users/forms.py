from django import forms
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm, PasswordChangeForm
from .models import Profile


class UserRegistrationForm(UserCreationForm):
    email = forms.EmailField(required=True)

    class Meta:
        model = User
        fields = ['username', 'first_name', 'last_name', 'email', 'password1', 'password2']


class UserUpdateForm(forms.ModelForm):
    email = forms.EmailField(required=True)

    class Meta:
        model = User
        fields = ['username', 'email', 'password']


class ProfileUpdateForm(forms.ModelForm):
    class Meta:
        model = Profile
        fields = '__all__'

class PasswordUpdate(PasswordChangeForm):
    email = forms.EmailField()

    class Meta:
        model = User
        fields = ['new_password1', 'new_password2']

        widgets = {
            'new_password1': forms.PasswordInput(attrs={'class': 'form-control', 'autocomplete': None}),
            'new_password2': forms.PasswordInput(attrs={'class': 'form-control', 'autocomplete': None}),

        }
