from django.db import models


class Stat(models.Model):
    """Stats counters shown in the brick-colored banner (e.g. 20+ Years in business)."""
    value = models.CharField(max_length=20, help_text="e.g. '20+', '100+'")
    label = models.CharField(max_length=100, help_text="e.g. 'Years in business'")
    order = models.PositiveIntegerField(default=0)

    class Meta:
        ordering = ['order']

    def __str__(self):
        return f"{self.value} — {self.label}"


class NewsItem(models.Model):
    """News/activity cards displayed on the homepage."""
    CATEGORY_CHOICES = [
        ('trust', 'Trust activity'),
        ('community', 'Community'),
        ('construction', 'Construction'),
        ('legal', 'Legal'),
        ('events', 'Events'),
    ]
    category = models.CharField(max_length=20, choices=CATEGORY_CHOICES, default='trust')
    title = models.CharField(max_length=200)
    description = models.TextField()
    link = models.URLField(blank=True, help_text="Optional link to full article")
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-created_at']

    def __str__(self):
        return self.title


class ContactEnquiry(models.Model):
    """Enquiries submitted through the contact form."""
    SERVICE_CHOICES = [
        ('construction', 'Construction'),
        ('trust', 'Bairava Trust / donation'),
        ('legal', 'Legal consultation'),
        ('events', 'Event management'),
    ]
    name = models.CharField(max_length=150)
    phone = models.CharField(max_length=20)
    service = models.CharField(max_length=20, choices=SERVICE_CHOICES)
    message = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-created_at']
        verbose_name_plural = 'Contact enquiries'

    def __str__(self):
        return f"{self.name} — {self.get_service_display()} ({self.created_at:%d %b %Y})"
