from django.contrib.auth.models import AbstractUser
from django.db import models

class User(AbstractUser):
    patronymic = models.CharField(blank=True, null=True, verbose_name="Отчество")