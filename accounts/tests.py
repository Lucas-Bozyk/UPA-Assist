from django.test import TestCase
from django.urls import reverse
from django.contrib.auth import get_user_model

class AccountsTests(TestCase):
    def test_register_page_status_code(self):
        response = self.client.get(reverse('register'))
        self.assertEqual(response.status_code, 200)

    def test_login_page_status_code(self):
        response = self.client.get(reverse('login'))
        self.assertEqual(response.status_code, 200)

    def test_create_user(self):
        User = get_user_model()
        user = User.objects.create_user(username='testuser', password='testpass123')
        self.assertEqual(user.username, 'testuser')

    def test_register_view_get(self):
        response = self.client.get(reverse('register'))
        self.assertEqual(response.status_code, 200)

    def test_register_view_post(self):
        data = {
            'username': 'newuser',
            'password1': 'complexpassword123',
            'password2': 'complexpassword123',
            'user_type': 'medico',
        }
        response = self.client.post(reverse('register'), data)
        self.assertEqual(response.status_code, 302)  # Redirect after successful registration
        User = get_user_model()
        self.assertTrue(User.objects.filter(username='newuser').exists())

    def test_medico_dashboard_view_access(self):
        User = get_user_model()
        medico = User.objects.create_user(username='meduser', password='testpass123', user_type='medico')
        self.client.login(username='meduser', password='testpass123')
        response = self.client.get(reverse('medico_dashboard'))
        self.assertEqual(response.status_code, 200)

    def test_medico_dashboard_view_dispatch_redirect(self):
        User = get_user_model()
        hospital = User.objects.create_user(username='hospitaluser', password='testpass123', user_type='hospital')
        self.client.login(username='hospitaluser', password='testpass123')
        response = self.client.get(reverse('medico_dashboard'))
        self.assertRedirects(response, reverse('hospital_dashboard'))

    def test_hospital_dashboard_view_access(self):
        User = get_user_model()
        hospital = User.objects.create_user(username='hospitaluser', password='testpass123', user_type='hospital')
        self.client.login(username='hospitaluser', password='testpass123')
        response = self.client.get(reverse('hospital_dashboard'))
        self.assertEqual(response.status_code, 200)

    def test_hospital_dashboard_view_dispatch_redirect(self):
        User = get_user_model()
        medico = User.objects.create_user(username='meduser', password='testpass123', user_type='medico')
        self.client.login(username='meduser', password='testpass123')
        response = self.client.get(reverse('hospital_dashboard'))
        self.assertRedirects(response, reverse('medico_dashboard'))

    def test_enfermeiro_dashboard_view_access(self):
        User = get_user_model()
        enfermeiro = User.objects.create_user(username='enfuser', password='testpass123', user_type='enfermeiro')
        self.client.login(username='enfuser', password='testpass123')
        response = self.client.get(reverse('enfermeiro_dashboard'))
        self.assertEqual(response.status_code, 200)

    def test_enfermeiro_dashboard_view_dispatch_redirect(self):
        User = get_user_model()
        medico = User.objects.create_user(username='meduser', password='testpass123', user_type='medico')
        self.client.login(username='meduser', password='testpass123')
        response = self.client.get(reverse('enfermeiro_dashboard'))
        self.assertRedirects(response, reverse('medico_dashboard'))

    def test_index_view(self):
        response = self.client.get(reverse('index'))
        self.assertEqual(response.status_code, 200)
