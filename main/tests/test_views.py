from django.test import TestCase, Client
from django.contrib.auth.models import User
from django.urls import reverse

class TestMainViews(TestCase):
    def setUp(self):
        self.client = Client()
        self.home_url = reverse('home')

    def test_home_can_access_page(self):
        response = self.client.get(self.home_url)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'main/home.html')  