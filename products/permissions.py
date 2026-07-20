from rest_framework import permissions

class IsAdminOrReadOnly(permissions.BasePermission):
    def has_permission(self, request, view):
        # Eğer gelen istek sadece "Okuma" (GET, HEAD, OPTIONS) ise herkese kapıyı aç
        if request.method in permissions.SAFE_METHODS:
            return True
        
        # Eğer istek "Yazma/Silme" ise, sadece giriş yapmış ve 'is_staff' (Yetkili) olanlara izin ver
        return bool(request.user and request.user.is_staff)