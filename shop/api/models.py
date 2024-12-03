from django.contrib.auth.models import AbstractUser
from django.db import models


# Create your models here.

class ApiUser(AbstractUser):
    balance = models.DecimalField(default=0, decimal_places=2, max_digits=10)  # Убедитесь, что max_digits достаточно


class Card(models.Model):
    issuingnetwork = models.CharField(max_length=64, default="")
    expired = models.CharField(max_length=7)  # Поле для хранения даты
    country = models.CharField(max_length=64)
    price = models.IntegerField(default=0)  # Исправлено значение по умолчанию
    purchased = models.BooleanField(default=False)
    purchased_user = models.ForeignKey(ApiUser, null=True, blank=True, on_delete=models.CASCADE, related_name="cards")
    card_number = models.CharField(max_length=16, blank=False, default="")
    CVV = models.IntegerField(blank=False, default=0)
    name = models.CharField(max_length=64)
    bank = models.CharField(max_length=64)
    address = models.CharField(max_length=64)

    def formatted_date(self):
        """Метод для отображения даты в формате MM/YYYY"""
        return self.expired.strftime('%m/%Y')

    def __str__(self):
        return str(self.card_number)


class Payment(models.Model):
    client = models.ForeignKey(ApiUser, on_delete=models.CASCADE)
    payment_address = models.CharField(max_length=64)
    invoice = models.CharField(max_length=64)
    payment_code = models.CharField(max_length=64)
    amount = models.DecimalField(max_digits=10, decimal_places=8)
    confirmations_required = models.IntegerField(default=1)
    status = models.CharField(max_length=20, default="pending")
    created_at = models.DateTimeField(auto_now_add=True)
