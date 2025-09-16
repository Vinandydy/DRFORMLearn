from django.urls import reverse

from main.models import *
from main.serializers import BookSerialzer
from rest_framework.test import APITestCase

class BooksApiTest(APITestCase):
    def test_get(self):
        book_1 = Book.objects.create(title = 'test', author=1, pubilsher=1, price=1000.00, published_year=2004)
        book_2 = Book.objects.create(title='test_2', author=2, pubilsher=2, price=2000.00, published_year=2004)
        url = reverse('book-list')
        response = self.client.get(url)
        serializer_data = BookSerialzer([book_1, book_2], many=True).data
        self.assertEqual(serializer_data, response.data)