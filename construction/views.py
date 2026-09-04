from django.shortcuts import render, redirect
from django.contrib import messages
from .models import Service, ConstructionProject
from .forms import ConstructionEnquiryForm


def project_list(request):
    """View to list all construction projects with category filter and custom enquiry form."""
    if request.method == 'POST':
        form = ConstructionEnquiryForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, 'Thank you! Your construction enquiry has been submitted. Our site engineer will reach out to you shortly.')
            return redirect('construction:project_list')
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
        'projects': projects,
        'services': Service.objects.all(),
        'categories': categories,
        'selected_category': category_filter,
        'form': form,
    }
    return render(request, 'construction/project_list.html', context)
