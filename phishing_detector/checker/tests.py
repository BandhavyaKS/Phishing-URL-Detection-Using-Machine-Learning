from django.test import TestCase
from django.urls import reverse

from model import MODEL, extract_features
from .models import URLCheck


class DashboardTests(TestCase):
    def test_dashboard_shows_recent_checks(self):
        URLCheck.objects.create(url='https://example.com', prediction='Legitimate')
        URLCheck.objects.create(url='https://fake-example.com', prediction='Phishing')

        response = self.client.get(reverse('dashboard'))

        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'Dashboard')
        self.assertContains(response, 'https://example.com')
        self.assertContains(response, 'Phishing')

    def test_model_uses_current_feature_count(self):
        features = extract_features('https://example.com')
        self.assertEqual(len(features), 15)
        self.assertEqual(MODEL.n_features_in_, 15)
