"""
URL configuration for bairava_project project.
"""
from django.contrib import admin
from django.urls import path, include, re_path
from django.conf import settings
from django.conf.urls.static import static
from django.views.static import serve

urlpatterns = [
    path('admin/', admin.site.urls),
    path('construction/', include('construction.urls')),
    path('trust/', include('trust.urls')),
    path('legal/', include('law_associates.urls')),
    path('events/', include('events.urls')),
    path('', include('core.urls')),
    re_path(r'^static/(?P<path>.*)$', serve, {'document_root': settings.STATIC_ROOT}),
    re_path(r'^media/(?P<path>.*)$', serve, {'document_root': settings.MEDIA_ROOT}),
]

admin.site.site_header = "Bairava Groups Admin Portal"
admin.site.site_title = "Bairava Groups"
admin.site.index_title = "Welcome to Bairava Groups Management"
