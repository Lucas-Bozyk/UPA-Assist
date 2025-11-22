from django import forms
from django.contrib.auth.forms import UserCreationForm
from .models import CustomUser, Paciente, Prontuario, ReceitaMedica
from django.forms import inlineformset_factory

class CustomUserRegistrationForm(UserCreationForm):
    USER_TYPE_CHOICES = (
        ('medico', 'Médico'),
        ('enfermeiro', 'Enfermeiro'),
    )
    user_type = forms.ChoiceField(choices=USER_TYPE_CHOICES, label="Tipo de usuário")

    class Meta:
        model = CustomUser
        fields = ['username', 'email', 'password1', 'password2', 'user_type']


class PacienteForm(forms.ModelForm):
    class Meta:
        model = Paciente
        fields = ['nome', 'data_nascimento']

        widgets = {
            'nome': forms.TextInput(attrs={'class': 'form-control'}),
            'data_nascimento': forms.DateInput(attrs={'class': 'form-control', 'type': 'date'}),
        }


class ProntuarioForm(forms.ModelForm):
    class Meta:
        model = Prontuario
        fields = ['paciente', 'sintomas', 'diagnostico']

        widgets = {
            'paciente': forms.Select(attrs={'class': 'form-control'}),
            'sintomas': forms.Textarea(attrs={'class': 'form-control'}),
            'diagnostico': forms.Textarea(attrs={'class': 'form-control'}),
        }


class ReceitaForm(forms.ModelForm):
    class Meta:
        model = ReceitaMedica
        fields = ['medicamento', 'dosagem', 'frequencia', 'duracao', 'observacoes']


ReceitaFormSet = inlineformset_factory(
    Prontuario,
    ReceitaMedica,
    form=ReceitaForm,
    extra=1,
    can_delete=True
)
