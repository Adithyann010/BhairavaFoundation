from django.contrib import admin
from .models import EventType, EventPortfolioItem, EventEnquiry


@admin.register(EventType)
class EventTypeAdmin(admin.ModelAdmin):
    list_display = ('title', 'order')
    list_editable = ('order',)


@admin.register(EventPortfolioItem)
class EventPortfolioItemAdmin(admin.ModelAdmin):
    list_display = ('title', 'location', 'category', 'guest_capacity', 'completion_year', 'order')
    list_filter = ('category', 'completion_year')
    search_fields = ('title', 'location', 'description')
    list_editable = ('order',)


@admin.register(EventEnquiry)
class EventEnquiryAdmin(admin.ModelAdmin):
    list_display = ('name', 'phone', 'event_type', 'event_date', 'expected_guests', 'created_at')
    list_filter = ('event_type', 'created_at')
    search_fields = ('name', 'phone', 'preferred_location', 'special_requirements')
    readonly_fields = ('created_at',)
