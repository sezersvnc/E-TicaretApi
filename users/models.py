import uuid
from django.db import models
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager

# 1. Kullanıcı Yaratıcısı (Manager)
class CustomUserManager(BaseUserManager):
    def create_user(self, email, password=None, **extra_fields):
        if not email:
            raise ValueError('Kullanıcıların bir e-posta adresi olmalıdır.')
        
        # E-postanın domain kısmını küçük harfe çevirir (normalize eder)
        email = self.normalize_email(email)
        user = self.model(email=email, **extra_fields)
        user.set_password(password) # Şifreyi hashleyerek güvenli hale getirir
        user.save(using=self._db)
        return user

    def create_superuser(self, email, password=None, **extra_fields):
        # Admin paneline girebilmesi için gerekli yetkileri veriyoruz
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)

        return self.create_user(email, password, **extra_fields)

# 2. Ana Kullanıcı Modeli (Giriş İşlemleri İçin)
class User(AbstractBaseUser):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    email = models.EmailField(max_length=255, unique=True)
    is_active = models.BooleanField(default=True)
    
    # Django admin paneli için gerekli olan standart alanlar
    is_staff = models.BooleanField(default=False)
    is_superuser = models.BooleanField(default=False)

    # Django'ya giriş için 'username' yerine 'email' kullanılacağını söylüyoruz
    USERNAME_FIELD = 'email'
    
    # Manager'ı modele bağlıyoruz
    objects = CustomUserManager()

    def __str__(self):
        return self.email

    # Admin panelindeki yetki kontrolleri için gereken temel fonksiyonlar
    def has_perm(self, perm, obj=None):
        return self.is_superuser

    def has_module_perms(self, app_label):
        return True

# 3. Profil Modeli (Detaylı Bilgiler İçin)
class Profile(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    # OneToOneField ile her kullanıcının sadece bir profili olmasını garanti ediyoruz
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='profile')
    address = models.TextField(blank=True, null=True)
    phone = models.CharField(max_length=20, blank=True, null=True)

    def __str__(self):
        return f"{self.user.email} - Profil"