from django.db import models


class Service(models.Model):
    """Construction & architecture service cards."""
    title = models.CharField(max_length=120)
    description = models.TextField()
    order = models.PositiveIntegerField(default=0)

    class Meta:
        ordering = ['order']

    def __str__(self):
        return self.title


class ConstructionProject(models.Model):
    """Portfolio of construction projects."""
    CATEGORY_CHOICES = [
        ('residential', 'Residential'),
        ('commercial', 'Commercial'),
        ('villas', 'Villas & Bungalows'),
        ('interiors', 'Interiors & Renovations'),
    ]

    STATUS_CHOICES = [
        ('completed', 'Completed'),
        ('ongoing', 'Ongoing'),
        ('upcoming', 'Upcoming'),
    ]

    title = models.CharField(max_length=200)
    location = models.CharField(max_length=150, help_text="e.g. Anna Nagar, Chennai")
    category = models.CharField(max_length=30, choices=CATEGORY_CHOICES, default='residential')
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='completed')
    description = models.TextField()
    completion_year = models.CharField(max_length=10, default="2024")
    built_up_area = models.CharField(max_length=50, blank=True, help_text="e.g. 4,500 sq.ft")
    image = models.ImageField(upload_to='projects/', blank=True, null=True)
    order = models.PositiveIntegerField(default=0)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['order', '-created_at']

    @property
    def static_image(self):
        slug = self.title.lower().strip()
        if 'height' in slug:
            return 'core/images/projects/bairava_heights.jpg'
        elif 'tech' in slug:
            return 'core/images/projects/bairava_tech_hub.jpg'
        elif 'villa' in slug:
            return 'core/images/projects/golden_villas.jpg'
        elif 'hq' in slug or 'renovation' in slug or 'corporate' in slug:
            return 'core/images/projects/corporate_hq.jpg'
        return 'core/images/divisions/construction.jpg'

    def __str__(self):
        return f"{self.title} ({self.location})"


class ConstructionEnquiry(models.Model):
    """Tailored enquiry for civil construction, architecture, and structural builds."""
    PROJECT_TYPE_CHOICES = [
        ('residential', 'Residential House'),
        ('commercial', 'Commercial Complex / Office'),
        ('villa', 'Independent Villa / Bungalow'),
        ('flat', 'Flat / Apartment Block'),
        ('interiors', 'Interiors & False Ceiling'),
        ('kitchen', 'Modular Kitchen'),
    ]

    name = models.CharField(max_length=150)
    phone = models.CharField(max_length=20)
    email = models.EmailField(blank=True)
    project_type = models.CharField(max_length=30, choices=PROJECT_TYPE_CHOICES)
    location = models.CharField(max_length=150, help_text="Site location in Chennai")
    plot_area = models.CharField(max_length=50, blank=True, help_text="e.g. 2,400 sq.ft")
    estimated_budget = models.CharField(max_length=50, blank=True, help_text="e.g. 50 Lakhs - 1 Crore")
    message = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-created_at']
        verbose_name_plural = 'Construction enquiries'

    def __str__(self):
        return f"{self.name} — {self.get_project_type_display()} ({self.location})"
