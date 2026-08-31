from django.contrib import admin
from .models import TrustProgram, TrustActivityItem, TrustEnquiry


@admin.register(TrustProgram)
class TrustProgramAdmin(admin.ModelAdmin):
    list_display = ('title', 'order')
    list_editable = ('order',)


@admin.register(TrustActivityItem)
class TrustActivityItemAdmin(admin.ModelAdmin):
    list_display = ('title', 'category', 'impact_stat', 'order')
    list_filter = ('category',)
    search_fields = ('title', 'description', 'impact_stat')
    list_editable = ('order',)


@admin.register(TrustEnquiry)
class TrustEnquiryAdmin(admin.ModelAdmin):
    list_display = ('name', 'phone', 'support_type', 'contribution_details', 'created_at')
    list_filter = ('support_type', 'created_at')
    search_fields = ('name', 'phone', 'contribution_details', 'message')
    readonly_fields = ('created_at',)
