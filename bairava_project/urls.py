"""
URL configuration for bairava_project project.
"""
from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('admin/', admin.site.urls),
    path('construction/', include('construction.urls')),
    path('trust/', include('trust.urls')),
    path('legal/', include('law_associates.urls')),
    path('events/', include('events.urls')),
    path('', include('core.urls')),
]

admin.site.site_header = "Bairava Groups Admin Portal"
admin.site.site_title = "Bairava Groups"
admin.site.index_title = "Welcome to Bairava Groups Management"

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
