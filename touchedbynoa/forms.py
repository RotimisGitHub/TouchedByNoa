from django import forms
from .models import Appointment, ContactUs
from datetime import time

class AppointmentForm(forms.ModelForm):
    class Meta:
        model = Appointment
        fields = ['title', 'size_and_price', 'length', 'date', 'time']

        widgets = {
            'date': forms.DateInput(
                attrs={
                    'type': 'date',
                    'class': 'form-control',


                }
            ),
            'time': forms.Select(attrs={
                'class': 'form-control',

            }),

            'size_and_price': forms.Select(attrs={
                'class': 'form-control'}),
            'length': forms.Select(attrs={
                'class': 'form-control'}),
            'title': forms.Select(attrs={'class': 'form-control'}),

        }



class ContactForm(forms.ModelForm):
    class Meta:
        model = ContactUs
        fields = ['name', 'email', 'client_message']

        widgets = {
            'name': forms.TextInput(attrs={'class': 'form-control'}),
            'client_message': forms.Textarea(attrs={'class': 'form-control'}),
            'email': forms.EmailInput(attrs={'class': 'form-control', 'type': 'email'}),
        }
