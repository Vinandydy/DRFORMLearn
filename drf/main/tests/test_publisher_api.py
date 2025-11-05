from rest_framework.test import APITestCase
from rest_framework import status
from django.urls import reverse

from main.tests.factories import *


class PublisherAPITest(APITestCase):
    def setUp(self):
        self.publisher1 = PublisherFactory()
        self.publisher2 = PublisherFactory()
        self.url = reverse("publisher-list")

    def test_get(self):
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 0)
