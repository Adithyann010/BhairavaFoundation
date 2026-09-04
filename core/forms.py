from django import forms
from .models import ContactEnquiry, DivisionEnquiry


class ContactEnquiryForm(forms.ModelForm):
    class Meta:
        model = ContactEnquiry
        fields = ['name', 'phone', 'email', 'service', 'message']
        widgets = {
            'name': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Your full name',
                'id': 'contact_name',
                'required': True,
            }),
            'phone': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': '+91 98765 43210',
                'id': 'contact_phone',
                'required': True,
            }),
            'email': forms.EmailInput(attrs={
                'class': 'form-control',
                'placeholder': 'your.email@example.com (optional)',
                'id': 'contact_email',
            }),
            'service': forms.Select(attrs={
                'class': 'form-control form-select',
                'id': 'contact_service',
            }),
            'message': forms.Textarea(attrs={
                'class': 'form-control',
                'placeholder': 'Tell us about your requirements or questions...',
                'rows': 4,
                'id': 'contact_message',
                'required': True,
            }),
        }
        labels = {
            'name': 'Full Name',
            'phone': 'Phone Number',
            'email': 'Email Address',
            'service': 'Enquiring About',
            'message': 'Your Message / Requirements',
        }


class DivisionEnquiryForm(forms.ModelForm):
    class Meta:
        model = DivisionEnquiry
        fields = ['name', 'phone', 'email', 'subject', 'message']
        widgets = {
            'name': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Your full name',
                'required': True,
            }),
            'phone': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': '+91 98765 43210',
                'required': True,
            }),
            'email': forms.EmailInput(attrs={
                'class': 'form-control',
                'placeholder': 'your.email@example.com (optional)',
            }),
            'subject': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Subject / Area of interest',
            }),
            'message': forms.Textarea(attrs={
                'class': 'form-control',
                'placeholder': 'Share your specific requirements or questions...',
                'rows': 4,
                'required': True,
            }),
        }
        labels = {
            'name': 'Full Name',
            'phone': 'Phone Number',
            'email': 'Email Address',
            'subject': 'Subject / Requirement',
            'message': 'Message Details',
        }

