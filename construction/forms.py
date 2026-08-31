from django import forms
from .models import ConstructionEnquiry


class ConstructionEnquiryForm(forms.ModelForm):
    class Meta:
        model = ConstructionEnquiry
        fields = ['name', 'phone', 'email', 'project_type', 'location', 'plot_area', 'estimated_budget', 'message']
        widgets = {
            'name': forms.TextInput(attrs={'placeholder': 'Your full name'}),
            'phone': forms.TextInput(attrs={'placeholder': '+91 Phone number'}),
            'email': forms.EmailInput(attrs={'placeholder': 'email@example.com (optional)'}),
            'project_type': forms.Select(),
            'location': forms.TextInput(attrs={'placeholder': 'e.g. Anna Nagar, Adyar, ECR'}),
            'plot_area': forms.TextInput(attrs={'placeholder': 'e.g. 2,400 sq.ft'}),
            'estimated_budget': forms.TextInput(attrs={'placeholder': 'e.g. ₹50L - ₹1Cr'}),
            'message': forms.Textarea(attrs={'placeholder': 'Describe your construction or architectural requirement', 'rows': 3}),
        }
