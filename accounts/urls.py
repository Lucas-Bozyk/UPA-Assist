from django.urls import path
from .views import RegisterView, MedicoDashboardView, HospitalDashboardView, EnfermeiroDashboardView, index, coverage_report
from django.contrib.auth.views import LoginView, LogoutView
from django.shortcuts import redirect
import logging

class CustomLoginView(LoginView):
    template_name = 'accounts/login.html'

    def get_success_url(self):
        user = self.request.user
        logging.info(f"User {user.username} logged in with user_type: {getattr(user, 'user_type', None)}")
        if user.user_type == 'medico':
            return '/medico/dashboard/'
        elif user.user_type == 'hospital':
            return '/hospital/dashboard/'
        elif user.user_type == 'enfermeiro':
            return '/enfermeiro/dashboard/'
        else:
            return super().get_success_url()

class CustomLogoutView(LogoutView):
    next_page = 'login'

urlpatterns = [
    path('', index, name='index'),
    path('login/', CustomLoginView.as_view(), name='login'),
    path('logout/', CustomLogoutView.as_view(), name='logout'),
    path('register/', RegisterView.as_view(), name='register'),
    path('medico/dashboard/', MedicoDashboardView.as_view(), name='medico_dashboard'),
    path('hospital/dashboard/', HospitalDashboardView.as_view(), name='hospital_dashboard'),
    path('enfermeiro/dashboard/', EnfermeiroDashboardView.as_view(), name='enfermeiro_dashboard'),
    path('coverage-report/<path:path>', coverage_report, name='coverage_report'),
    path('coverage-report/', coverage_report, name='coverage_report_index'),
]
