from django.db import models
import uuid
from products.models import Products
from django.conf import settings
# Create your models here.
class Order(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    user= models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='user',null=True)
    total_amount=models.DecimalField(max_digits=10, decimal_places=2, default=0.00)
    STATUS_CHOICES = (
        ('Bekliyor', 'Bekliyor'),
        ('Hazırlanıyor', 'Hazırlanıyor'),
        ('Kargolandı', 'Kargolandı'),
        ('Tamamlandı', 'Tamamlandı'),
    )
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='Bekliyor')
    def __str__(self):
        return f"Sipariş{self.id}-{self.user.email}"
class OrderItem(models.Model):
    id=models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    order = models.ForeignKey(Order, on_delete=models.CASCADE, related_name='items',null=True)
    product = models.ForeignKey(Products, on_delete=models.CASCADE,null=True)
    quantity=models.IntegerField(default=1)
    def __str__(self):
        return f"{self.quantity} adet {self.product.name}"