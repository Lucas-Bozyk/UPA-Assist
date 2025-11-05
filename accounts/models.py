from django.contrib.auth.models import AbstractUser
from django.db import models
from django.conf import settings

class CustomUser(AbstractUser):
    USER_TYPE_CHOICES = (
        ('hospital', 'Hospital'),
        ('medico', 'Médico'),
        ('enfermeiro', 'Enfermeiro'),
    )
    user_type = models.CharField(max_length=20, choices=USER_TYPE_CHOICES, default='enfermeiro')




