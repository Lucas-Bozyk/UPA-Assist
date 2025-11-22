from django import forms
from .models import Paciente, Prontuario


class PacienteForm(forms.ModelForm):
    class Meta:
        model = Paciente
        fields = ['nome', 'cpf', 'data_nascimento']

        widgets = {
            'nome': forms.TextInput(attrs={'class': 'form-control'}),
            'cpf': forms.TextInput(attrs={'class': 'form-control'}),
            'data_nascimento': forms.DateInput(attrs={'class': 'form-control', 'type': 'date'}),
        }


class ProntuarioForm(forms.ModelForm):
    class Meta:
        model = Prontuario
        fields = [
            'paciente',
            'queixa_principal',
            'historico',
            'exame_fisico',
            'conduta'
        ]

        widgets = {
            'paciente': forms.Select(attrs={'class': 'form-control'}),
            'queixa_principal': forms.Textarea(attrs={'class': 'form-control'}),
            'historico': forms.Textarea(attrs={'class': 'form-control'}),
            'exame_fisico': forms.Textarea(attrs={'class': 'form-control'}),
            'conduta': forms.Textarea(attrs={'class': 'form-control'}),
        }


from .models import ReceitaMedica
from django.forms import inlineformset_factory


#Receita Médica
class ReceitaForm(forms.ModelForm):
    class Meta:
        model = ReceitaMedica
        fields = ['medicamento', 'dosagem', 'frequencia', 'duracao', 'observacoes']


# Permite adicionar várias receitas no mesmo atendimento
ReceitaFormSet = inlineformset_factory(
    Prontuario,
    ReceitaMedica,
    form=ReceitaForm,
    extra=1,             # começa com 1 receita
    can_delete=True
)
