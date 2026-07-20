from django.urls import path
from . import views

urlpatterns = [
    # Kullanıcı '/api/orders/' adresine geldiğinde 'siparis_listesi' fonksiyonu çalışacak
    
    path('orders/', views.siparis_listesi, name='siparis-listesi'),
    path('orders/add-item/', views.siparis_kalemi_ekle, name='siparis-kalemi-ekle'),
]