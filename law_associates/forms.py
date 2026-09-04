from django import forms
from .models import LegalEnquiry


class LegalEnquiryForm(forms.ModelForm):
    class Meta:
        model = LegalEnquiry
        fields = ['name', 'phone', 'email', 'issue_type', 'urgency', 'brief_details']
        widgets = {
            'name': forms.TextInput(attrs={'placeholder': 'Your full name'}),
            'phone': forms.TextInput(attrs={'placeholder': '+91 Phone number'}),
            'email': forms.EmailInput(attrs={'placeholder': 'email@example.com (optional)'}),
            'issue_type': forms.Select(),
            'urgency': forms.Select(),
            'brief_details': forms.Textarea(attrs={'placeholder': 'Describe your legal situation confidentially', 'rows': 3}),
        }
