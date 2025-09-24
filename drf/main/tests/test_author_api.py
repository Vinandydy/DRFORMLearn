from rest_framework.test import APITestCase
from rest_framework import status
from django.urls import reverse

from main.tests.factories import *




class AuthorAPITest(APITestCase):
    def setUp(self):
        self.author1 = AuthorFactory()
        self.author2 = AuthorFactory()
        self.author3 = AuthorFactory()
        self.author_url = reverse('author-list')

    def test_author_list(self):
        response = self.client.get(self.author_url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 0)

    def test_find(self):
        BookFactory(author=self.author1, title='smth', published_year=2000, price=50)
        BookFactory(author=self.author1, title='smth', published_year=2000, price=150)
        BookFactory(author=self.author2, title='smth', published_year=2000, price=200)
        BookFactory(author=self.author2, title='smth', published_year=2000, price=2000)
        self.find_url = reverse('author-find')
        data={
            'author_a': self.author1,
            'author_b': self.author2,
            'price_a': 150,
            'price_b': 250
        }
        response = self.client.post(self.find_url, data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

        self.assertEqual(len(response.data), 2)

