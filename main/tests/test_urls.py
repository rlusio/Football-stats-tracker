from django.urls import reverse, resolve
from django.test import TestCase
from main.views import home

class TestMainURLs(TestCase):
    def test_main_url(self):
        url = reverse('/main/home')
        self.assertEqual(resolve(url).func, home)