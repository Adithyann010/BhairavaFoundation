from django.urls import path
from . import views

app_name = 'core'

urlpatterns = [
    path('', views.home, name='home'),
    path('enquiries/', views.all_enquiries, name='all_enquiries'),
]
