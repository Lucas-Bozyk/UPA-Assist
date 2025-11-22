from django.views.generic import CreateView, TemplateView
from django.views import View
from django.urls import reverse_lazy
from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import redirect, render, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.views.static import serve
from .models import CustomUser, Paciente, Prontuario
from .forms import (
    CustomUserRegistrationForm,
    PacienteForm,
    ProntuarioForm,
    ReceitaFormSet
)
import os


# =========================================
# CADASTRO DE USUÁRIO
# =========================================
class RegisterView(CreateView):
    model = CustomUser
    form_class = CustomUserRegistrationForm
    template_name = 'accounts/register.html'
    success_url = reverse_lazy('login')


# =========================================
# DASHBOARD DO MÉDICO
# =========================================
class MedicoDashboardView(LoginRequiredMixin, TemplateView):
    template_name = 'accounts/medico_dashboard.html'

    def dispatch(self, request, *args, **kwargs):
        if request.user.user_type != 'medico':
            return redirect('hospital_dashboard')
        return super().dispatch(request, *args, **kwargs)


# =========================================
# ETAPA 1 — CADASTRO DO PACIENTE
# =========================================
class PacienteCreateView(View):
    template_name = "accounts/atendimento_paciente.html"

    def get(self, request):
        form = PacienteForm()
        return render(request, self.template_name, {"form": form})

    def post(self, request):
        form = PacienteForm(request.POST)
        if form.is_valid():
            paciente = form.save()
            return redirect('atendimento_prontuario', paciente_id=paciente.id)

        return render(request, self.template_name, {"form": form})


# =========================================
# ETAPA 2 — CADASTRO DO PRONTUÁRIO
# =========================================
class ProntuarioCreateView(View):
    template_name = "accounts/atendimento_prontuario.html"

    def get(self, request, paciente_id):
        paciente = get_object_or_404(Paciente, id=paciente_id)
        form = ProntuarioForm(initial={'paciente': paciente})
        return render(request, self.template_name, {
            "form": form,
            "paciente": paciente
        })

    def post(self, request, paciente_id):
        paciente = get_object_or_404(Paciente, id=paciente_id)
        form = ProntuarioForm(request.POST)

        if form.is_valid():
            prontuario = form.save(commit=False)
            prontuario.paciente = paciente
            prontuario.save()

            return redirect('atendimento_receitas', prontuario_id=prontuario.id)

        return render(request, self.template_name, {
            "form": form,
            "paciente": paciente
        })


# =========================================
# ETAPA 3 — CADASTRO DAS RECEITAS
# =========================================
class ReceitaCreateView(View):
    template_name = "accounts/atendimento_receitas.html"

    def get(self, request, prontuario_id):
        prontuario = get_object_or_404(Prontuario, id=prontuario_id)
        formset = ReceitaFormSet(instance=prontuario)
        return render(request, self.template_name, {
            "formset": formset,
            "prontuario": prontuario
        })

    def post(self, request, prontuario_id):
        prontuario = get_object_or_404(Prontuario, id=prontuario_id)
        formset = ReceitaFormSet(request.POST, instance=prontuario)

        if formset.is_valid():
            formset.save()
            return redirect('medico_dashboard')

        return render(request, self.template_name, {
            "formset": formset,
            "prontuario": prontuario
        })


# =========================================
# REDIRECIONAMENTO PADRÃO
# =========================================
def index(request):
    return redirect('login')


# =========================================
# SERVIDOR DO RELATÓRIO DE COBERTURA
# =========================================
@login_required
def coverage_report(request, path=''):
    coverage_dir = os.path.join(
        os.path.dirname(os.path.dirname(os.path.abspath(__file__))),
        'htmlcov'
    )

    if path == '' or path.endswith('/'):
        path = 'index.html'

    full_path = os.path.join(coverage_dir, path)

    if not os.path.exists(full_path):
        raise Http404("Coverage report file not found")

    return serve(request, path, document_root=coverage_dir)
