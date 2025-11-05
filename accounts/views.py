from django.views.generic import CreateView, TemplateView
from django.urls import reverse_lazy
from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import redirect, render
from .models import CustomUser
from .forms import CustomUserRegistrationForm
from django.contrib.auth.decorators import login_required, user_passes_test
from django.views.static import serve
import os

class RegisterView(CreateView):
    model = CustomUser
    form_class = CustomUserRegistrationForm
    template_name = 'accounts/register.html'
    success_url = reverse_lazy('login')  # Redireciona para login após cadastro

class MedicoDashboardView(LoginRequiredMixin, TemplateView):
    template_name = 'accounts/medico_dashboard.html'

    def dispatch(self, request, *args, **kwargs):
        if request.user.user_type != 'medico':
            return redirect('hospital_dashboard')
        return super().dispatch(request, *args, **kwargs)

class HospitalDashboardView(LoginRequiredMixin, TemplateView):
    template_name = 'accounts/hospital_dashboard.html'

    def dispatch(self, request, *args, **kwargs):
        if request.user.user_type != 'hospital':
            return redirect('medico_dashboard')
        return super().dispatch(request, *args, **kwargs)

class EnfermeiroDashboardView(LoginRequiredMixin, TemplateView):
    template_name = 'accounts/enfermeiro_dashboard.html'

    def dispatch(self, request, *args, **kwargs):
        if request.user.user_type != 'enfermeiro':
            return redirect('medico_dashboard')
        return super().dispatch(request, *args, **kwargs)

def index(request):
    return render(request, 'accounts/index.html')

from django.http import Http404

@login_required
def coverage_report(request, path=''):
    coverage_dir = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), 'htmlcov')
    if path == '' or path.endswith('/'):
        path = 'index.html'
    full_path = os.path.join(coverage_dir, path)
    if not os.path.exists(full_path):
        raise Http404("Coverage report file not found")
    return serve(request, path, document_root=coverage_dir)
