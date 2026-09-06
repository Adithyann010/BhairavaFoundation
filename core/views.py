from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from django.http import Http404

from construction.models import Service as ConstructionService, ConstructionProject, ConstructionEnquiry
from construction.forms import ConstructionEnquiryForm
from trust.models import TrustProgram, TrustActivityItem, TrustEnquiry
from trust.forms import TrustEnquiryForm
from law_associates.models import LegalService, LegalPracticeDetail, LegalEnquiry
from events.models import EventType, EventPortfolioItem, EventEnquiry
from events.forms import EventEnquiryForm
from core.models import (
    Stat, NewsItem, ContactEnquiry, BusinessDivision,
    DivisionOffering, DivisionGalleryItem, MediaArticle, DivisionEnquiry
)
from .forms import ContactEnquiryForm, DivisionEnquiryForm


def home(request):
    """Render the main homepage with hero, about, 9 businesses grid, spotlight, and quick contact."""
    if request.method == 'POST':
        form = ContactEnquiryForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, 'Thank you! Your enquiry has been submitted. Our team will get back to you shortly.')
            return redirect('core:home')
    else:
        form = ContactEnquiryForm()

    divisions = BusinessDivision.objects.filter(is_active=True).order_by('order')
    commercial_divisions = divisions.filter(division_type='business')
    foundation_divisions = divisions.filter(division_type='foundation_trust')

    context = {
        'divisions': divisions,
        'commercial_divisions': commercial_divisions,
        'foundation_divisions': foundation_divisions,
        'stats': Stat.objects.all(),
        'news_items': NewsItem.objects.all()[:4],
        'featured_projects': ConstructionProject.objects.all()[:3],
        'trust_activities': TrustActivityItem.objects.all()[:3],
        'event_portfolio': EventPortfolioItem.objects.all()[:3],
        'form': form,
    }
    return render(request, 'core/home.html', context)


def about_view(request):
    """Dedicated About Bairava Groups page."""
    context = {
        'divisions': BusinessDivision.objects.filter(is_active=True),
        'stats': Stat.objects.all(),
    }
    return render(request, 'core/about.html', context)


def contact_view(request):
    """Dedicated Contact Us page with contact form, details, and map."""
    if request.method == 'POST':
        form = ContactEnquiryForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, 'Thank you! Your message has been received. Our team will reach out promptly.')
            return redirect('core:contact')
    else:
        initial_service = request.GET.get('division', 'general')
        form = ContactEnquiryForm(initial={'service': initial_service})

    context = {
        'form': form,
        'divisions': BusinessDivision.objects.filter(is_active=True),
    }
    return render(request, 'core/contact.html', context)


def businesses_index(request):
    """Directory overview of all 9 business divisions and initiatives."""
    divisions = BusinessDivision.objects.filter(is_active=True).order_by('order')
    context = {
        'divisions': divisions,
        'commercial_divisions': divisions.filter(division_type='business'),
        'foundation_divisions': divisions.filter(division_type='foundation_trust'),
    }
    return render(request, 'core/businesses_index.html', context)


def future_plan_view(request):
    """Dedicated Future Plan page showcasing upcoming ventures under Bairava Groups."""
    upcoming_businesses = [
        {
            'name': 'Bairava Water Solutions',
            'slug': 'water-solutions',
            'category': 'Future Business / Upcoming Venture',
            'tagline': 'Pure Water. Healthier Lives.',
            'main_concept': 'Packaged drinking water and water-can distribution.',
            'description': 'Bairava Water Solutions will focus on providing high-quality packaged drinking water and water-can distribution, serving homes, offices and businesses with convenient and reliable delivery.',
            'supporting_points': [
                'Packaged Drinking Water',
                'Water Can Distribution',
                'Home Delivery',
                'Office & Business Supply',
                'Reliable Distribution',
                'Convenient Service'
            ],
            'feature_items': [
                'Clean & Safe Drinking Water',
                'Home & Office Delivery',
                'For Individuals & Businesses',
                'Reliable & Convenient Service'
            ],
            'bottom_message': 'A Healthier Tomorrow with Bairava.',
            'static_image': 'core/images/divisions/water_solutions.jpg',
            'theme': 'water'
        },
        {
            'name': 'Bairava Jewellery',
            'slug': 'jewellery',
            'category': 'Future Business / Upcoming Venture',
            'tagline': 'Timeless Beauty. Lasting Value.',
            'main_concept': 'Jewellery retail and collections.',
            'description': 'Bairava Jewellery will bring elegant and high-quality jewellery collections that combine traditional inspiration with modern design, created for meaningful moments and special occasions.',
            'supporting_points': [
                'Gold Jewellery',
                'Traditional Collections',
                'Contemporary Designs',
                'Elegant Craftsmanship',
                'Special Occasion Collections',
                'Customer-focused Experience'
            ],
            'feature_items': [
                'Elegant Collections',
                'Quality Craftsmanship',
                'Traditional & Modern Designs',
                'For Every Special Occasion'
            ],
            'bottom_message': 'Tradition Today. For Generations Tomorrow.',
            'static_image': 'core/images/divisions/jewellery.jpg',
            'theme': 'jewellery'
        }
    ]

    context = {
        'upcoming_businesses': upcoming_businesses,
    }
    return render(request, 'core/future_plan.html', context)



def foundation_view(request):
    """Dedicated page for Bairava Foundation."""
    division = get_object_or_404(BusinessDivision, slug='foundation')
    if request.method == 'POST':
        form = DivisionEnquiryForm(request.POST)
        if form.is_valid():
            enquiry = form.save(commit=False)
            enquiry.division = division
            enquiry.save()
            messages.success(request, 'Thank you for connecting with Bairava Foundation. We will be in touch shortly.')
            return redirect('core:foundation')
    else:
        form = DivisionEnquiryForm()

    context = {
        'division': division,
        'offerings': division.offerings.all(),
        'form': form,
    }
    return render(request, 'core/foundation.html', context)


def business_detail(request, slug):
    """Serve dedicated pages for individual business divisions."""
    division = get_object_or_404(BusinessDivision, slug=slug)

    # Route specialized existing apps if accessed via /businesses/<slug>/
    if slug == 'foundation':
        return foundation_view(request)
    elif slug == 'construction':
        return construction_division_view(request, division)
    elif slug == 'event-management':
        return events_division_view(request, division)
    elif slug == 'trust':
        return redirect('trust:index')

    if request.method == 'POST':
        form = DivisionEnquiryForm(request.POST)
        if form.is_valid():
            enquiry = form.save(commit=False)
            enquiry.division = division
            enquiry.save()
            messages.success(request, f'Thank you! Your enquiry for {division.name} has been submitted successfully.')
            return redirect('core:business_detail', slug=slug)
    else:
        form = DivisionEnquiryForm()

    template_map = {
        'finance': 'core/divisions/finance.html',
        'cloud-kitchen': 'core/divisions/cloud_kitchen.html',
        'sports-club': 'core/divisions/sports_club.html',
        'aadukalam': 'core/divisions/aadukalam.html',
        'media': 'core/divisions/media.html',
    }

    template_name = template_map.get(slug, 'core/divisions/generic_division.html')

    extra_context = {}
    if slug == 'media':
        extra_context['articles'] = MediaArticle.objects.all()
    elif slug == 'finance':
        extra_context['solutions'] = division.offerings.all()
    elif slug == 'cloud-kitchen':
        extra_context['menu_items'] = division.offerings.all()
    elif slug == 'sports-club':
        extra_context['facilities'] = division.offerings.all()
    elif slug == 'aadukalam':
        extra_context['activities'] = division.offerings.all()

    context = {
        'division': division,
        'offerings': division.offerings.all(),
        'form': form,
        **extra_context
    }
    return render(request, template_name, context)


def construction_division_view(request, division):
    """Render Construction division within the unified businesses framework."""
    if request.method == 'POST':
        form = ConstructionEnquiryForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, 'Thank you! Your construction enquiry has been submitted. Our engineering team will contact you shortly.')
            return redirect('core:business_detail', slug='construction')
    else:
        form = ConstructionEnquiryForm()

    category_filter = request.GET.get('category', '')
    projects = ConstructionProject.objects.all()
    if category_filter:
        projects = projects.filter(category=category_filter)

    categories = [
        ('', 'All Projects'),
        ('residential', 'Residential'),
        ('commercial', 'Commercial'),
        ('villas', 'Villas & Bungalows'),
        ('interiors', 'Interiors & Renovations'),
    ]

    context = {
        'division': division,
        'projects': projects,
        'services': ConstructionService.objects.all(),
        'categories': categories,
        'selected_category': category_filter,
        'form': form,
    }
    return render(request, 'construction/project_list.html', context)


def events_division_view(request, division):
    """Render Event Management division within the unified businesses framework."""
    if request.method == 'POST':
        form = EventEnquiryForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, 'Thank you! Your event enquiry has been received. Our coordinator will contact you shortly.')
            return redirect('core:business_detail', slug='event-management')
    else:
        form = EventEnquiryForm()

    category_filter = request.GET.get('category', '')
    portfolio_items = EventPortfolioItem.objects.all()
    if category_filter:
        portfolio_items = portfolio_items.filter(category=category_filter)

    categories = [
        ('', 'All Events'),
        ('wedding', 'Weddings & Receptions'),
        ('corporate', 'Corporate & Summits'),
        ('social', 'Social Celebrations'),
        ('decor', 'Decor & Floral'),
    ]

    context = {
        'division': division,
        'event_types': EventType.objects.all(),
        'portfolio_items': portfolio_items,
        'categories': categories,
        'selected_category': category_filter,
        'form': form,
    }
    return render(request, 'events/index.html', context)


def all_enquiries(request):
    """Unified dashboard view displaying all enquiries received across all forms."""
    context = {
        'contact_enquiries': ContactEnquiry.objects.all(),
        'division_enquiries': DivisionEnquiry.objects.all(),
        'construction_enquiries': ConstructionEnquiry.objects.all(),
        'trust_enquiries': TrustEnquiry.objects.all(),
        'legal_enquiries': LegalEnquiry.objects.all(),
        'event_enquiries': EventEnquiry.objects.all(),
    }
    return render(request, 'core/all_enquiries.html', context)

