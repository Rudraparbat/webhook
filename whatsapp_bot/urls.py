
from django.contrib import admin
from django.urls import path , include
from whatsapp_bot.views import WhatsAppWebhookAPIView

urlpatterns = [
    
    path("" , WhatsAppWebhookAPIView.as_view() , name = "whatsappbot")
]
