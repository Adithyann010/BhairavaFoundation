from django.db import models


class EventType(models.Model):
    """Event type tiles (Weddings, Corporate events, etc.)."""
    title = models.CharField(max_length=120)
    description = models.CharField(max_length=255)
    order = models.PositiveIntegerField(default=0)

    class Meta:
        ordering = ['order']

    def __str__(self):
        return self.title


class EventPortfolioItem(models.Model):
    """Portfolio showcase of past and ongoing managed events."""
    CATEGORY_CHOICES = [
        ('wedding', 'Weddings & Receptions'),
        ('corporate', 'Corporate & Conferences'),
        ('social', 'Social Galas & Parties'),
        ('decor', 'Custom Decor & Floral'),
    ]

    title = models.CharField(max_length=200)
    location = models.CharField(max_length=150, help_text="e.g. ECR Beach Resort, Guindy Hotel")
    category = models.CharField(max_length=30, choices=CATEGORY_CHOICES, default='wedding')
    guest_capacity = models.CharField(max_length=50, blank=True, help_text="e.g. 600 Guests")
    completion_year = models.CharField(max_length=10, default="2024")
    description = models.TextField()
    image = models.ImageField(upload_to='events/', blank=True, null=True)
    order = models.PositiveIntegerField(default=0)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['order', '-created_at']
        verbose_name_plural = 'Event portfolio items'

    def __str__(self):
        return f"{self.title} ({self.location})"


class EventEnquiry(models.Model):
    """Tailored enquiry for wedding, corporate, and social event planning."""
    EVENT_TYPE_CHOICES = [
        ('wedding', 'Wedding Ceremony & Reception'),
        ('corporate', 'Corporate Conference / Product Launch'),
        ('social', 'Birthday / Family Gathering'),
        ('vendor', 'Vendor Sourcing (Catering / Decor / Photo)'),
        ('day_of', 'Day-of Event Coordination'),
    ]

    name = models.CharField(max_length=150)
    phone = models.CharField(max_length=20)
    email = models.EmailField(blank=True)
    event_type = models.CharField(max_length=30, choices=EVENT_TYPE_CHOICES)
    event_date = models.CharField(max_length=50, blank=True, help_text="Proposed date or month")
    expected_guests = models.CharField(max_length=50, blank=True, help_text="e.g. 500 guests")
    preferred_location = models.CharField(max_length=150, blank=True, help_text="e.g. ECR Beach Resort, Hotel in Guindy")
    special_requirements = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-created_at']
        verbose_name_plural = 'Event enquiries'

    def __str__(self):
        return f"{self.name} — {self.get_event_type_display()} ({self.expected_guests})"
