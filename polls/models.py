from django.db import models

#Model Paciente
class Paciente(models.Model):
    nome = models.CharField(max_length=150)
    cpf = models.CharField(max_length=14, unique=True, db_index=True)
    data_nascimento = models.DateField()

    def __str__(self):
        return f"{self.nome} ({self.cpf})"

#Classe Prontuario
class Prontuario(models.Model):
    paciente = models.ForeignKey(
        Paciente,
        on_delete=models.CASCADE,
        to_field='cpf',          # A FK usa o CPF em vez do ID
        db_column='paciente_cpf' # Nome da coluna no banco (opcional mas recomendado)
    )

    queixa_principal = models.TextField()
    historico = models.TextField(blank=True, null=True)
    exame_fisico = models.TextField(blank=True, null=True)
    conduta = models.TextField()

    data_atendimento = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Prontuário de {self.paciente.nome} - {self.data_atendimento.strftime('%d/%m/%Y')}"
    

    
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
