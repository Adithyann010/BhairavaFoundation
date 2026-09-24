from django.shortcuts import redirect


def legal_index(request):
    """Route /legal/ to Bairava Law Associates business page."""
    return redirect('core:business_detail', slug='law-associates', permanent=True)


