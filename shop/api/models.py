from django.contrib.auth.models import AbstractUser
from django.db import models


# Create your models here.

class ApiUser(AbstractUser):
    balance = models.DecimalField(default=0, decimal_places=2, max_digits=10)  # Убедитесь, что max_digits достаточно


class Base(models.Model):
    name = models.CharField(max_length=64)

    def __str__(self):
        return self.name


class Company(models.Model):
    name = models.CharField(max_length=64)

    def __str__(self):
        return self.name


class Card(models.Model):
    BIN = models.IntegerField(default=8)  # Исправлено значение по умолчанию
    Base = models.ForeignKey(Base, on_delete=models.CASCADE, related_name='cards')
    expired = models.DateField()  # Поле для хранения даты
    city = models.CharField(max_length=64)
    state = models.CharField(max_length=64)
    ZIP_code = models.CharField(max_length=64)
    country = models.CharField(max_length=64)
    Company = models.ForeignKey(Company, on_delete=models.CASCADE, related_name='cards')
    price = models.IntegerField(default=0)  # Исправлено значение по умолчанию
    bank = models.CharField(max_length=64, default="")
    purchased = models.BooleanField(default=False)
    purchased_user = models.ForeignKey(ApiUser, null=True, blank=True, on_delete=models.CASCADE, related_name="cards")
    card_number = models.CharField(max_length=19, blank=False, default="")
    CVV = models.IntegerField(blank=False, default=0)

    def formatted_date(self):
        """Метод для отображения даты в формате MM/YYYY"""
        return self.expired.strftime('%m/%Y')

    def __str__(self):
        return str(self.BIN)


class Checked_card(models.Model):
    card = models.ForeignKey(Card, on_delete=models.CASCADE, related_name="Checked_card")
    address = models.CharField(max_length=64, default="")
    city = models.CharField(max_length=64, default="")
    lastName = models.CharField(max_length=64, default="")
    firstName = models.CharField(max_length=64, default="")
    postcode = models.CharField(max_length=64, default="")
    code = models.CharField(max_length=12)
    status = models.BooleanField(default=False)
