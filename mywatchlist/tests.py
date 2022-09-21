from django.test import TestCase, Client
from django.urls import reverse

# Create your tests here.
class MyWatchlistResponseTest(TestCase):
    def setUp(self):
        self.client = Client()
        
    def test_html(self):
        response = self.client.get(reverse('show_html'))
        self.assertEquals(response.status_code, 200)

    def test_xml(self):
        response = self.client.get(reverse('show_xml'))
        self.assertEquals(response.status_code, 200)

    def test_json(self):
        response = self.client.get(reverse('show_json'))
        self.assertEquals(response.status_code, 200)