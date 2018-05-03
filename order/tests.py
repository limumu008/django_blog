from django.test import TestCase

from django.urls import reverse


class TestOrderCreateView(TestCase):
    def test_form_invalid(self):
        self.client.post(reverse('order:create_order'), )
