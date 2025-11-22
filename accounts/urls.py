from django.urls import path
from .views import (
    RegisterView,
    MedicoDashboardView,
    index,
    coverage_report,
    PacienteCreateView,
    ProntuarioCreateView,
    ReceitaCreateView,
)
from django.contrib.auth.views import LoginView, LogoutView
import logging


class CustomLoginView(LoginView):
    template_name = 'accounts/login.html'

    def get_success_url(self):
        user = self.request.user
        logging.info(f"User {user.username} logged in with user_type: {getattr(user, 'user_type', None)}")
        
        if user.user_type == 'medico':
            return '/medico/dashboard/'
        
        return super().get_success_url()


class CustomLogoutView(LogoutView):
    next_page = 'login'


urlpatterns = [
    path('', index, name='index'),
    
    # login / logout / register
    path('login/', CustomLoginView.as_view(), name='login'),
    path('logout/', CustomLogoutView.as_view(), name='logout'),
    path('register/', RegisterView.as_view(), name='register'),

    # dashboard
    path('medico/dashboard/', MedicoDashboardView.as_view(), name='medico_dashboard'),

    # fluxo de atendimento dividido
    path('atendimento/paciente/', PacienteCreateView.as_view(), name='atendimento_paciente'),
    path('atendimento/prontuario/<int:paciente_id>/', ProntuarioCreateView.as_view(), name='atendimento_prontuario'),
    path('atendimento/receitas/<int:prontuario_id>/', ReceitaCreateView.as_view(), name='atendimento_receitas'),

    # coverage
    path('coverage-report/<path:path>', coverage_report, name='coverage_report'),
    path('coverage-report/', coverage_report, name='coverage_report_index'),
]
