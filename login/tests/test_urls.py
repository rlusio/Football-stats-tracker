from django.urls import reverse, resolve
from django.test import TestCase
from login import views
from django.contrib.auth import views as auth_views

class TestLoginURLs(TestCase):
    def test_register_url(self):
        url = reverse('login:register')
        self.assertEqual(resolve(url).func, views.register)

    def test_login_url(self):
        url = reverse('login:login')
        self.assertEqual(resolve(url).func.view_class, auth_views.LoginView)

    def test_logout_url(self):
        url = reverse('login:logout')
        self.assertEqual(resolve(url).func.view_class, auth_views.LogoutView)