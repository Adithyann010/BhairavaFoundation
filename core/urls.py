from django.urls import path
from . import views
from . import views_chat

app_name = 'core'

urlpatterns = [
    path('', views.home, name='home'),
    path('about/', views.about_view, name='about'),
    path('contact/', views.contact_view, name='contact'),
    path('foundation/', views.foundation_view, name='foundation'),
    path('future-plan/', views.future_plan_view, name='future_plan'),
    path('businesses/', views.businesses_index, name='businesses_index'),
    path('businesses/<slug:slug>/', views.business_detail, name='business_detail'),
    path('enquiries/', views.all_enquiries, name='all_enquiries'),
    
    # AI Chatbot API Endpoints
    path('api/chat/', views_chat.chat_api, name='chat_api'),
    path('api/chat/suggestions/', views_chat.chat_suggestions_api, name='chat_suggestions_api'),
]


