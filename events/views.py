from django.shortcuts import render, redirect
from django.contrib import messages
from .models import EventType, EventPortfolioItem
from .forms import EventEnquiryForm


def events_index(request):
    """View for Event Management showcase and booking form."""
    if request.method == 'POST':
        form = EventEnquiryForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, 'Thank you! Your event enquiry has been received. Our event coordinator will get in touch shortly.')
            return redirect('events:index')
    else:
        form = EventEnquiryForm()

    category_filter = request.GET.get('category', '')
    portfolio_items = EventPortfolioItem.objects.all()
    if category_filter:
        portfolio_items = portfolio_items.filter(category=category_filter)

    categories = [
        ('', 'All Events'),
        ('wedding', 'Weddings'),
        ('corporate', 'Corporate'),
        ('social', 'Social Galas'),
        ('decor', 'Decor & Floral'),
    ]

    context = {
        'event_types': EventType.objects.all(),
        'portfolio_items': portfolio_items,
        'categories': categories,
        'selected_category': category_filter,
        'form': form,
    }
    return render(request, 'events/index.html', context)
