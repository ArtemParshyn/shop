from django.contrib.auth.models import AbstractUser
from django.db import models


# Create your models here.

class ApiUser(AbstractUser):
    ...


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
    price = models.IntegerField(default=8)  # Исправлено значение по умолчанию
    bank = models.CharField(max_length=64, default="")

    def formatted_date(self):
        """Метод для отображения даты в формате MM/YYYY"""
        return self.expired.strftime('%m/%Y')

    def __str__(self):
        return str(self.BIN)
