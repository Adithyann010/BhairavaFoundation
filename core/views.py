from django.shortcuts import render, redirect
from django.contrib import messages

from construction.models import Service, ConstructionEnquiry
from trust.models import TrustProgram, TrustEnquiry
from law_associates.models import LegalService, LegalEnquiry
from events.models import EventType, EventEnquiry
from core.models import Stat, NewsItem, ContactEnquiry
from .forms import ContactEnquiryForm


def home(request):
    """Render the single-page homepage with all sections and handle the general contact form."""
    if request.method == 'POST':
        form = ContactEnquiryForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, 'Thank you! Your enquiry has been submitted. We will get back to you shortly.')
            return redirect('core:home')
    else:
        form = ContactEnquiryForm()

    context = {
        'services': Service.objects.all(),
        'trust_programs': TrustProgram.objects.all(),
        'legal_services': LegalService.objects.all(),
        'event_types': EventType.objects.all(),
        'stats': Stat.objects.all(),
        'news_items': NewsItem.objects.all()[:3],
        'form': form,
    }
    return render(request, 'core/home.html', context)


def all_enquiries(request):
    """Unified dashboard view displaying all enquiries received across all 5 forms."""
    context = {
        'contact_enquiries': ContactEnquiry.objects.all(),
        'construction_enquiries': ConstructionEnquiry.objects.all(),
        'trust_enquiries': TrustEnquiry.objects.all(),
        'legal_enquiries': LegalEnquiry.objects.all(),
        'event_enquiries': EventEnquiry.objects.all(),
    }
    return render(request, 'core/all_enquiries.html', context)
