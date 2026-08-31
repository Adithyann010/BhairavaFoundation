from django.contrib import admin
from .models import Stat, NewsItem, ContactEnquiry


@admin.register(Stat)
class StatAdmin(admin.ModelAdmin):
    list_display = ('value', 'label', 'order')
    list_editable = ('order',)


@admin.register(NewsItem)
class NewsItemAdmin(admin.ModelAdmin):
    list_display = ('title', 'category', 'created_at')
    list_filter = ('category',)


@admin.register(ContactEnquiry)
class ContactEnquiryAdmin(admin.ModelAdmin):
    list_display = ('name', 'phone', 'service', 'created_at')
    list_filter = ('service', 'created_at')
    readonly_fields = ('created_at',)
