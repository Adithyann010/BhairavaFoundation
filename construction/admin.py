from django.contrib import admin
from .models import Service, ConstructionProject, ConstructionEnquiry


@admin.register(Service)
class ServiceAdmin(admin.ModelAdmin):
    list_display = ('title', 'order')
    list_editable = ('order',)


@admin.register(ConstructionProject)
class ConstructionProjectAdmin(admin.ModelAdmin):
    list_display = ('title', 'slug', 'location', 'category', 'status', 'built_up_area', 'completion_year', 'order')
    list_filter = ('category', 'status')
    search_fields = ('title', 'slug', 'location', 'description')
    prepopulated_fields = {'slug': ('title',)}
    list_editable = ('order',)


@admin.register(ConstructionEnquiry)
class ConstructionEnquiryAdmin(admin.ModelAdmin):
    list_display = ('name', 'phone', 'project_type', 'location', 'plot_area', 'created_at')
    list_filter = ('project_type', 'created_at')
    search_fields = ('name', 'phone', 'location', 'message')
    readonly_fields = ('created_at',)
