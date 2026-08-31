from django.contrib import admin
from .models import LegalService, LegalPracticeDetail, LegalEnquiry


@admin.register(LegalService)
class LegalServiceAdmin(admin.ModelAdmin):
    list_display = ('description', 'tag', 'order')
    list_editable = ('order',)


@admin.register(LegalPracticeDetail)
class LegalPracticeDetailAdmin(admin.ModelAdmin):
    list_display = ('title', 'category', 'turnaround_time', 'order')
    list_filter = ('category',)
    search_fields = ('title', 'description')
    list_editable = ('order',)


@admin.register(LegalEnquiry)
class LegalEnquiryAdmin(admin.ModelAdmin):
    list_display = ('name', 'phone', 'issue_type', 'urgency', 'created_at')
    list_filter = ('issue_type', 'urgency', 'created_at')
    search_fields = ('name', 'phone', 'brief_details')
    readonly_fields = ('created_at',)
