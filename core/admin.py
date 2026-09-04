from django.contrib import admin
from .models import (
    Stat, NewsItem, ContactEnquiry,
    BusinessDivision, DivisionOffering, DivisionGalleryItem,
    MediaArticle, DivisionEnquiry
)


class DivisionOfferingInline(admin.TabularInline):
    model = DivisionOffering
    extra = 1


class DivisionGalleryItemInline(admin.TabularInline):
    model = DivisionGalleryItem
    extra = 1


@admin.register(BusinessDivision)
class BusinessDivisionAdmin(admin.ModelAdmin):
    list_display = ('name', 'slug', 'division_type', 'order', 'is_active')
    list_editable = ('order', 'is_active')
    list_filter = ('division_type', 'is_active')
    search_fields = ('name', 'tagline', 'short_description')
    prepopulated_fields = {'slug': ('name',)}
    inlines = [DivisionOfferingInline, DivisionGalleryItemInline]


@admin.register(DivisionOffering)
class DivisionOfferingAdmin(admin.ModelAdmin):
    list_display = ('title', 'division', 'badge', 'order')
    list_filter = ('division',)
    search_fields = ('title', 'description')
    list_editable = ('order',)


@admin.register(DivisionGalleryItem)
class DivisionGalleryItemAdmin(admin.ModelAdmin):
    list_display = ('title', 'division', 'order')
    list_filter = ('division',)
    search_fields = ('title', 'caption')
    list_editable = ('order',)


@admin.register(MediaArticle)
class MediaArticleAdmin(admin.ModelAdmin):
    list_display = ('title', 'category', 'publish_date', 'featured', 'order')
    list_filter = ('category', 'featured')
    search_fields = ('title', 'summary', 'content')
    prepopulated_fields = {'slug': ('title',)}
    list_editable = ('featured', 'order')


@admin.register(Stat)
class StatAdmin(admin.ModelAdmin):
    list_display = ('value', 'label', 'order')
    list_editable = ('order',)


@admin.register(NewsItem)
class NewsItemAdmin(admin.ModelAdmin):
    list_display = ('title', 'category', 'created_at')
    list_filter = ('category',)
    search_fields = ('title', 'description')


@admin.register(ContactEnquiry)
class ContactEnquiryAdmin(admin.ModelAdmin):
    list_display = ('name', 'phone', 'email', 'service', 'created_at')
    list_filter = ('service', 'created_at')
    search_fields = ('name', 'phone', 'email', 'message')
    readonly_fields = ('created_at',)


@admin.register(DivisionEnquiry)
class DivisionEnquiryAdmin(admin.ModelAdmin):
    list_display = ('name', 'division', 'phone', 'email', 'created_at')
    list_filter = ('division', 'created_at')
    search_fields = ('name', 'phone', 'email', 'message', 'subject')
    readonly_fields = ('created_at',)

