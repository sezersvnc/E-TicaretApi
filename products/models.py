from django.db import models
import uuid

# Create your models here.
from django.db import models
import uuid

# 1. Önce Kategori sınıfı tanımlanmalı
class Category(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    title=models.CharField(max_length=100)
    # 'Blank' parametresinin baş harfi küçük harfe (blank) çevrildi:
    slug=models.SlugField(null=False, blank=True, unique=True, db_index=True, editable=False)
    def __str__(self):
        return f"{self.title}"

# 2. Sonra Ürünler sınıfı tanımlanmalı
class Products(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    name=models.CharField(max_length=255)
    price=models.DecimalField(max_digits=10, decimal_places=2)
    stock=models.IntegerField()
    category = models.ForeignKey(Category, on_delete=models.CASCADE, related_name='Products')