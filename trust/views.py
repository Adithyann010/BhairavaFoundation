from django.shortcuts import render, redirect
from django.contrib import messages
from .models import TrustProgram, TrustActivityItem
from .forms import TrustEnquiryForm


def trust_index(request):
    """View for Bairava Trust activities, elder care, and donation info."""
    if request.method == 'POST':
        form = TrustEnquiryForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, 'Blessings! Thank you for offering to support Bairava Charitable Trust. We will contact you shortly.')
            return redirect('trust:index')
    else:
        form = TrustEnquiryForm()

    category_filter = request.GET.get('category', '')
    activity_items = TrustActivityItem.objects.all()
    if category_filter:
        activity_items = activity_items.filter(category=category_filter)

    categories = [
        ('', 'All Initiatives'),
        ('annadhanam', 'Annadhanam (Free Meals)'),
        ('elder_care', 'Elder Care Shelter'),
        ('scholarship', 'Scholarships'),
        ('relief', 'Community Relief'),
    ]

    context = {
        'trust_programs': TrustProgram.objects.all(),
        'activity_items': activity_items,
        'categories': categories,
        'selected_category': category_filter,
        'form': form,
    }
    return render(request, 'trust/index.html', context)
