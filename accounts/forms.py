from django import forms
from django.contrib.auth.forms import UserCreationForm
from .models import CustomUser

class CustomUserRegistrationForm(UserCreationForm):
    USER_TYPE_CHOICES = (
        ('medico', 'Médico'),
        ('enfermeiro', 'Enfermeiro'),
    )
    user_type = forms.ChoiceField(choices=USER_TYPE_CHOICES, label="Tipo de usuário")

    class Meta:
        model = CustomUser
        fields = ['username', 'email', 'password1', 'password2', 'user_type']



