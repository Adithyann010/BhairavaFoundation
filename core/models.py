from django.db import models


class Stat(models.Model):
    """Stats counters shown in the group overview banner."""
    value = models.CharField(max_length=20, help_text="e.g. '20+', '100+'")
    label = models.CharField(max_length=100, help_text="e.g. 'Years of Excellence'")
    order = models.PositiveIntegerField(default=0)

    class Meta:
        ordering = ['order']

    def __str__(self):
        return f"{self.value} — {self.label}"


class NewsItem(models.Model):
    """News/activity cards displayed on the homepage and media highlights."""
    CATEGORY_CHOICES = [
        ('trust', 'TRUST ACTIVITY'),
        ('community', 'COMMUNITY'),
        ('construction', 'CONSTRUCTION'),
        ('legal', 'LEGAL'),
        ('events', 'EVENTS'),
        ('sports', 'SPORTS & YOUTH'),
        ('media', 'MEDIA & PRESS'),
        ('general', 'GROUP UPDATE'),
    ]
    category = models.CharField(max_length=20, choices=CATEGORY_CHOICES, default='trust')
    title = models.CharField(max_length=200)
    description = models.TextField()
    link = models.URLField(blank=True, help_text="Optional link to full article")
    image = models.ImageField(upload_to='news/', blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-created_at']

    def __str__(self):
        return self.title


class BusinessDivision(models.Model):
    """Core model representing each of the 9 Bairava Groups divisions."""
    DIVISION_TYPE_CHOICES = [
        ('business', 'COMMERCIAL BUSINESS'),
        ('foundation_trust', 'FOUNDATION & SOCIAL INITIATIVE'),
    ]

    name = models.CharField(max_length=150)
    slug = models.SlugField(max_length=100, unique=True)
    tagline = models.CharField(max_length=255, blank=True)
    short_description = models.TextField(help_text="Short description shown on cards/homepage")
    full_description = models.TextField(blank=True, help_text="In-depth about description on dedicated page")
    division_type = models.CharField(max_length=30, choices=DIVISION_TYPE_CHOICES, default='business')
    icon_name = models.CharField(max_length=50, blank=True, help_text="Lucide/SVG icon identifier")
    hero_image = models.ImageField(upload_to='divisions/', blank=True, null=True)
    static_image_path = models.CharField(max_length=255, blank=True, help_text="Fallback static image path")
    accent_color = models.CharField(max_length=20, default='#7C3B29')
    target_url = models.CharField(max_length=200, blank=True, help_text="Target URL if custom routed")
    order = models.PositiveIntegerField(default=0)
    is_active = models.BooleanField(default=True)

    class Meta:
        ordering = ['order', 'name']
        verbose_name = 'Business Division'
        verbose_name_plural = 'Business Divisions'

    def __str__(self):
        return self.name


class DivisionOffering(models.Model):
    """Services, activities, menu items, or practice areas under a business division."""
    division = models.ForeignKey(BusinessDivision, on_delete=models.CASCADE, related_name='offerings')
    title = models.CharField(max_length=150)
    badge = models.CharField(max_length=60, blank=True, help_text="e.g. 'Popular', 'Organic', 'Certified'")
    description = models.TextField()
    icon = models.CharField(max_length=50, blank=True)
    order = models.PositiveIntegerField(default=0)

    class Meta:
        ordering = ['order', 'title']

    def __str__(self):
        return f"{self.division.name} — {self.title}"


class DivisionGalleryItem(models.Model):
    """Photo gallery item for a business division."""
    division = models.ForeignKey(BusinessDivision, on_delete=models.CASCADE, related_name='gallery_items')
    title = models.CharField(max_length=150)
    caption = models.CharField(max_length=255, blank=True)
    image = models.ImageField(upload_to='division_gallery/', blank=True, null=True)
    static_image_path = models.CharField(max_length=255, blank=True)
    order = models.PositiveIntegerField(default=0)

    class Meta:
        ordering = ['order']

    def __str__(self):
        return f"{self.division.name} Gallery: {self.title}"


class MediaArticle(models.Model):
    """News, stories, and media releases for Bairava Media."""
    title = models.CharField(max_length=220)
    slug = models.SlugField(max_length=120, unique=True)
    category = models.CharField(max_length=80, default="PRESS RELEASE")
    summary = models.TextField()
    content = models.TextField(blank=True)
    publish_date = models.DateField(auto_now_add=True)
    image = models.ImageField(upload_to='media_articles/', blank=True, null=True)
    static_image_path = models.CharField(max_length=255, blank=True)
    featured = models.BooleanField(default=False)
    order = models.PositiveIntegerField(default=0)

    class Meta:
        ordering = ['-publish_date', 'order']

    def __str__(self):
        return self.title


class ContactEnquiry(models.Model):
    """General contact enquiries submitted through the website."""
    SERVICE_CHOICES = [
        ('general', 'GENERAL ENQUIRY'),
        ('foundation', 'BAIRAVA FOUNDATION'),
        ('finance', 'BAIRAVA FINANCE'),
        ('construction', 'BAIRAVA CONSTRUCTION & LAND PROMOTERS'),
        ('cloud_kitchen', 'BAIRAVA CLOUD KITCHEN'),
        ('sports_club', 'BAIRAVA SPORTS CLUB'),
        ('event_management', 'BAIRAVA EVENT MANAGEMENT'),
        ('aadukalam', 'BAIRAVA AADUKALAM'),
        ('trust', 'BAIRAVA TRUST'),
        ('media', 'BAIRAVA MEDIA'),
        ('association', 'BHAIRAVA ASSOCIATION'),
        ('legal', 'LEGAL CONSULTATION'),
    ]
    name = models.CharField(max_length=150)
    phone = models.CharField(max_length=20)
    email = models.EmailField(blank=True)
    service = models.CharField(max_length=30, choices=SERVICE_CHOICES, default='general')
    message = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-created_at']
        verbose_name_plural = 'Contact enquiries'

    def __str__(self):
        return f"{self.name} — {self.get_service_display()} ({self.created_at:%d %b %Y})"


class DivisionEnquiry(models.Model):
    """Dedicated enquiry submitted on an individual business page."""
    division = models.ForeignKey(BusinessDivision, on_delete=models.CASCADE, related_name='enquiries')
    name = models.CharField(max_length=150)
    phone = models.CharField(max_length=20)
    email = models.EmailField(blank=True)
    subject = models.CharField(max_length=200, blank=True)
    requirement_type = models.CharField(max_length=100, blank=True)
    message = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-created_at']
        verbose_name = 'Division Enquiry'
        verbose_name_plural = 'Division Enquiries'

    def __str__(self):
        return f"{self.name} — {self.division.name} ({self.created_at:%d %b %Y})"
