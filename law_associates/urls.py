from django.urls import path
from . import views

app_name = 'law_associates'

urlpatterns = [
    path('', views.legal_index, name='index'),
]
