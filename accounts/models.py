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

class Paciente(models.Model):
    nome = models.CharField(max_length=100)
    data_nascimento = models.DateField()

    def __str__(self):
        return self.nome

class Prontuario(models.Model):
    paciente = models.ForeignKey(Paciente, on_delete=models.CASCADE)
    data = models.DateTimeField(auto_now_add=True)
    sintomas = models.TextField()
    diagnostico = models.TextField()

    def __str__(self):
        return f"Prontuário de {self.paciente.nome}"

class ReceitaMedica(models.Model):
    prontuario = models.ForeignKey(
        Prontuario,
        on_delete=models.CASCADE,
        related_name='receitas'
    )
    medicamento = models.CharField(max_length=150)
    dosagem = models.CharField(max_length=100)
    frequencia = models.CharField(max_length=100)
    duracao = models.CharField(max_length=100, blank=True, null=True)
    observacoes = models.TextField(blank=True, null=True)

    def __str__(self):
        return f"{self.medicamento} - {self.prontuario.paciente.nome}"