from django import forms
from django.contrib.auth.forms import UserCreationForm, PasswordChangeForm
from django.contrib.auth import get_user_model

User = get_user_model()

class UserRegistrationForm(UserCreationForm):
    email = forms.EmailField(required=True)

    class Meta:
        model = User
        fields = ['email', 'password1', 'password2']

class LoginForm(forms.Form):
    email = forms.EmailField()
    password = forms.CharField(widget=forms.PasswordInput())

class UserUpdateForm(forms.ModelForm):
    email = forms.EmailField(required=True)

    class Meta:
        model = User
        fields = ['email', 'password']




class PasswordUpdate(PasswordChangeForm):
    email = forms.EmailField()

    class Meta:
        model = User
        fields = ['new_password1', 'new_password2']

        widgets = {
            'new_password1': forms.PasswordInput(attrs={'class': 'form-field-text', 'autocomplete': None}),
            'new_password2': forms.PasswordInput(attrs={'class': 'form-field-text', 'autocomplete': None}),

        }
