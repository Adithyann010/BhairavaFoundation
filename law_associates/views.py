from django.shortcuts import redirect


def legal_index(request):
    """Safely redirect legacy /legal/ route to the businesses directory."""
    return redirect('core:businesses_index', permanent=True)

