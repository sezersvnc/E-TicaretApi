from django.contrib import admin
from .models import User, Profile

class CustomUserAdmin(admin.ModelAdmin):
    # Admin panelindeki listede hangi sütunların görüneceğini belirliyoruz
    list_display = ('email', 'is_staff', 'is_superuser', 'is_active')
    search_fields = ('email',)

    # Admin panelinden yeni kullanıcı kaydedilirken şifrenin hashlenmesi için araya giriyoruz
    def save_model(self, request, obj, form, change):
        # Eğer girilen şifre zaten hashlenmemişse (düz metinse), onu hash'e çevir
        if obj.password and not obj.password.startswith('pbkdf2_'):
            obj.set_password(obj.password)
        
        # Standart kaydetme işlemine devam et
        super().save_model(request, obj, form, change)

# Yazdığımız bu özel kuralları modele bağlayarak admin paneline kaydediyoruz
admin.site.register(User, CustomUserAdmin)

# Profil modelini de standart olarak ekleyelim
admin.site.register(Profile)