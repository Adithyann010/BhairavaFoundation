from django import forms
from .models import ContactEnquiry


class ContactEnquiryForm(forms.ModelForm):
    class Meta:
        model = ContactEnquiry
        fields = ['name', 'phone', 'service', 'message']
        widgets = {
            'name': forms.TextInput(attrs={
                'placeholder': 'Your name',
                'id': 'fname',
            }),
            'phone': forms.TextInput(attrs={
                'placeholder': '+91',
                'id': 'fphone',
            }),
            'service': forms.Select(attrs={
                'id': 'fservice',
            }),
            'message': forms.Textarea(attrs={
                'placeholder': 'Tell us a bit about what you need',
                'id': 'fmsg',
            }),
        }
        labels = {
            'name': 'Full name',
            'phone': 'Phone number',
            'service': "I'm enquiring about",
            'message': 'Message',
        }
