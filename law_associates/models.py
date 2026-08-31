from django.db import models


class LegalService(models.Model):
    """Legal service line items with tags (Notices, Recovery, Property, etc.)."""
    description = models.CharField(max_length=255)
    tag = models.CharField(max_length=50, help_text="e.g. 'Notices', 'Recovery', 'Property'")
    order = models.PositiveIntegerField(default=0)

    class Meta:
        ordering = ['order']

    def __str__(self):
        return f"{self.description} [{self.tag}]"


class LegalPracticeDetail(models.Model):
    """Detailed legal practice area cards for showcase."""
    CATEGORY_CHOICES = [
        ('notice', 'Legal Notices & Replies'),
        ('property', 'Property Due Diligence & Titles'),
        ('recovery', 'Money Recovery & Cheque Bounce'),
        ('criminal', 'Criminal Defense & Bail'),
        ('protection', 'Recovery Agent Protection'),
    ]

    title = models.CharField(max_length=200)
    category = models.CharField(max_length=30, choices=CATEGORY_CHOICES, default='notice')
    turnaround_time = models.CharField(max_length=100, blank=True, help_text="e.g. 24 - 48 Hour Opinion")
    description = models.TextField()
    order = models.PositiveIntegerField(default=0)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['order', '-created_at']
        verbose_name_plural = 'Legal practice details'

    def __str__(self):
        return self.title


class LegalEnquiry(models.Model):
    """Tailored enquiry for legal advocacy, notice consultation, and court representation."""
    ISSUE_TYPE_CHOICES = [
        ('notice', 'Legal Notice Consultation'),
        ('property', 'Property Verification & Due Diligence'),
        ('recovery', 'Money Recovery Case'),
        ('criminal', 'Criminal Defense & Bail'),
        ('protection', 'Harassment / Recovery Agent Protection'),
        ('opinion', 'General Legal Opinion'),
    ]

    URGENCY_CHOICES = [
        ('immediate', 'Immediate / Court Notice Received'),
        ('urgent', 'Within 3 Days'),
        ('general', 'General Advice'),
    ]

    name = models.CharField(max_length=150)
    phone = models.CharField(max_length=20)
    email = models.EmailField(blank=True)
    issue_type = models.CharField(max_length=30, choices=ISSUE_TYPE_CHOICES)
    urgency = models.CharField(max_length=20, choices=URGENCY_CHOICES, default='urgent')
    brief_details = models.TextField(help_text="Brief description of the legal matter")
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-created_at']
        verbose_name_plural = 'Legal enquiries'

    def __str__(self):
        return f"{self.name} — {self.get_issue_type_display()} ({self.get_urgency_display()})"
