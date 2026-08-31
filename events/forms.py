from django import forms
from .models import EventEnquiry


class EventEnquiryForm(forms.ModelForm):
    class Meta:
        model = EventEnquiry
        fields = ['name', 'phone', 'email', 'event_type', 'event_date', 'expected_guests', 'preferred_location', 'special_requirements']
        widgets = {
            'name': forms.TextInput(attrs={'placeholder': 'Your full name'}),
            'phone': forms.TextInput(attrs={'placeholder': '+91 Phone number'}),
            'email': forms.EmailInput(attrs={'placeholder': 'email@example.com (optional)'}),
            'event_type': forms.Select(),
            'event_date': forms.TextInput(attrs={'placeholder': 'e.g. Dec 2024 / Nov 15'}),
            'expected_guests': forms.TextInput(attrs={'placeholder': 'e.g. 300 - 500 guests'}),
            'preferred_location': forms.TextInput(attrs={'placeholder': 'e.g. ECR, Nungambakkam, Guindy'}),
            'special_requirements': forms.Textarea(attrs={'placeholder': 'Tell us about your decor, catering, or venue preferences', 'rows': 3}),
        }
