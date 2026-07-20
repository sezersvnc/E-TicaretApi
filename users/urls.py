from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import UserViewSet

router = DefaultRouter()
# 'users' adında bir endpoint açıyoruz
router.register(r'users', UserViewSet)

urlpatterns = [
    path('', include(router.urls)),
]