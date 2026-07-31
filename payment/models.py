
# Create your models here.
from django.db import models
import uuid
from orders.models import Order

class PaymentStatus(models.TextChoices):
    PENDING = "pending", "Beklemede"
    PROCESSING = "processing", "İşleniyor"
    SUCCEEDED = "succeeded", "Başarılı"
    FAILED = "failed", "Başarısız"
    CANCELLED = "cancelled", "İptal Edildi"
    REFUNDED = "refunded", "İade Edildi"


class PaymentMethod(models.TextChoices):
    CREDIT_CARD = "credit_card", "Kredi Kartı"
    DEBIT_CARD = "debit_card", "Banka Kartı"
    WALLET = "wallet", "Cüzdan"
    BANK_TRANSFER = "bank_transfer", "Havale/EFT"
    CASH_ON_DELIVERY = "cash_on_delivery", "Kapıda Ödeme"

class Payment(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    order = models.ForeignKey(Order,on_delete=models.PROTECT,related_name="payments")
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    currency = models.CharField(max_length=3, default="TRY")

    status = models.CharField(
        max_length=20,
        choices=PaymentStatus.choices,
        default=PaymentStatus.PENDING,
    )

    method = models.CharField(
        max_length=30,
        choices=PaymentMethod.choices,
        null=True,
        blank=True,
    )

    # Hangi sağlayıcı kullanılırsa kullanılsın (henüz yok), oradan dönen
    # ham veriyi/özel alanları burada JSON olarak saklıyoruz.
    provider = models.CharField(max_length=50, null=True, blank=True)  # örn: "iyzico", "stripe"
    provider_reference = models.CharField(max_length=255, null=True, blank=True)  # işlem/transaction id
    raw_data = models.JSONField(default=dict, blank=True)  # sağlayıcıdan dönecek ham response

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    paid_at = models.DateTimeField(null=True, blank=True)

    class Meta:
        ordering = ["-created_at"]

    def __str__(self):
        return f"{self.order_id} - {self.amount} {self.currency} ({self.status})"