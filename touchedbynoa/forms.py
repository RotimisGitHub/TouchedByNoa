from django import forms
from django.utils import timezone

from .models import Appointment, ContactUs
from datetime import time


class DatePickerWidget(forms.DateInput):
    def get_context(self, name, value, attrs):
        context = super().get_context(name, value, attrs)
        context['widget']['attrs']['min'] = timezone.now().strftime('%Y-%m-%d')
        return context

class AppointmentForm(forms.ModelForm):
    class Meta:
        model = Appointment
        fields = ['title', 'size_and_price', 'length', 'date', 'time']

        widgets = {
            'date': DatePickerWidget(
                attrs={
                    'type': 'date',
                    'class': 'form-field-text',
                }
            ),

            'time': forms.Select(attrs={
                'class': 'form-field-text',

            }),

            'size_and_price': forms.Select(attrs={
                'class': 'form-field-text'}),
            'length': forms.Select(attrs={
                'class': 'form-field-text'}),
            'title': forms.Select(attrs={'class': 'form-field-text'}),

        }

        def clean_future_date(self):
            future_date = self.cleaned_data.get('date')

            # Check if the selected date is in the future
            if future_date and future_date <= timezone.now().date():
                raise forms.ValidationError("Please select a date in the future.")



class ContactForm(forms.ModelForm):
    class Meta:
        model = ContactUs
        fields = ['name', 'email', 'client_message']

        widgets = {
            'name': forms.TextInput(attrs={'class': 'form-field-text'}),
            'client_message': forms.Textarea(attrs={'class': 'form-field-text'}),
            'email': forms.EmailInput(attrs={'class': 'form-field-text', 'type': 'email'}),
        }
