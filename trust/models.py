from django.db import models


class TrustProgram(models.Model):
    """Trust programs (Annadhanam, Elder care, Scholarships)."""
    title = models.CharField(max_length=120)
    description = models.TextField()
    order = models.PositiveIntegerField(default=0)

    class Meta:
        ordering = ['order']

    def __str__(self):
        return self.title


class TrustActivityItem(models.Model):
    """Showcase of trust activities, relief drives, and community care."""
    CATEGORY_CHOICES = [
        ('annadhanam', 'Annadhanam (Daily Meals)'),
        ('elder_care', 'Elder Care Shelter'),
        ('scholarship', 'Educational Scholarships'),
        ('relief', 'Community Relief & Festivals'),
    ]

    title = models.CharField(max_length=200)
    category = models.CharField(max_length=30, choices=CATEGORY_CHOICES, default='annadhanam')
    impact_stat = models.CharField(max_length=100, blank=True, help_text="e.g. 500+ Free Meals Served Daily")
    description = models.TextField()
    image = models.ImageField(upload_to='trust/', blank=True, null=True)
    order = models.PositiveIntegerField(default=0)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['order', '-created_at']
        verbose_name_plural = 'Trust activity items'

    def __str__(self):
        return self.title


class TrustEnquiry(models.Model):
    """Tailored enquiry/sponsorship form for Bairava Charitable Trust."""
    SUPPORT_TYPE_CHOICES = [
        ('annadhanam', 'Annadhanam (Daily Meal Sponsorship)'),
        ('elder_care', 'Elder Care & Medical Support'),
        ('scholarship', 'Educational Scholarship Support'),
        ('volunteer', 'Volunteer & Service'),
        ('general', 'General Donation / Support'),
    ]

    name = models.CharField(max_length=150)
    phone = models.CharField(max_length=20)
    email = models.EmailField(blank=True)
    support_type = models.CharField(max_length=30, choices=SUPPORT_TYPE_CHOICES)
    contribution_details = models.CharField(max_length=150, blank=True, help_text="e.g. Birthday Annadhanam, Rs 5000/month")
    message = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-created_at']
        verbose_name_plural = 'Trust enquiries'

    def __str__(self):
        return f"{self.name} — {self.get_support_type_display()}"
