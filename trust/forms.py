from django import forms
from .models import TrustEnquiry


class TrustEnquiryForm(forms.ModelForm):
    class Meta:
        model = TrustEnquiry
        fields = ['name', 'phone', 'email', 'support_type', 'contribution_details', 'message']
        widgets = {
            'name': forms.TextInput(attrs={'placeholder': 'Your full name'}),
            'phone': forms.TextInput(attrs={'placeholder': '+91 Phone number'}),
            'email': forms.EmailInput(attrs={'placeholder': 'email@example.com (optional)'}),
            'support_type': forms.Select(),
            'contribution_details': forms.TextInput(attrs={'placeholder': 'e.g. Birthday Meal Sponsorship / Monthly Support'}),
            'message': forms.Textarea(attrs={'placeholder': 'How would you like to contribute or volunteer?', 'rows': 3}),
        }
