from django.shortcuts import render, redirect
from django.contrib import messages
from .models import LegalService, LegalPracticeDetail
from .forms import LegalEnquiryForm


def legal_index(request):
    """View for Legal Associates advocacy & consultation practice."""
    if request.method == 'POST':
        form = LegalEnquiryForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, 'Confidential enquiry received. Our advocate will review your matter and contact you promptly.')
            return redirect('law_associates:index')
    else:
        form = LegalEnquiryForm()

    category_filter = request.GET.get('category', '')
    practice_details = LegalPracticeDetail.objects.all()
    if category_filter:
        practice_details = practice_details.filter(category=category_filter)

    categories = [
        ('', 'All Practice Areas'),
        ('notice', 'Legal Notices'),
        ('property', 'Property Due Diligence'),
        ('recovery', 'Money Recovery'),
        ('criminal', 'Criminal Defense'),
        ('protection', 'Recovery Protection'),
    ]

    context = {
        'legal_services': LegalService.objects.all(),
        'practice_details': practice_details,
        'categories': categories,
        'selected_category': category_filter,
        'form': form,
    }
    return render(request, 'law_associates/index.html', context)
