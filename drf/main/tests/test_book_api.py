from rest_framework.test import APITestCase
from rest_framework import status
from django.urls import reverse

from main.tests.factories import *


class BookAPITest(APITestCase):
    def setUp(self):
        self.book1 = BookFactory()
        self.book2 = BookFactory()
        self.book_url = reverse('book-list')

    def test_get_book(self):
        response = self.client.get(self.book_url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 2)

    def test_retrieve_book(self):
        detail_url = reverse('book-detail', kwargs={'pk': self.book1.pk})
        response = self.client.get(detail_url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['title'], self.book1.title)

    def test_create_book(self):
        author = AuthorFactory()
        publisher = PublisherFactory()
        book_count = Book.objects.count()
        data = {
            'title': "Test 1",
            'author': author.id,
            'publisher': publisher.id,
            'price': '100.00',
            'published_year': 2020
        }
        response = self.client.post(self.book_url, data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Book.objects.count(), book_count + 1)

    def test_update_book(self):
        update_url = reverse('book-detail', kwargs={'pk': self.book1.pk})
        data = {
            'title': 'New Title',
            'price': '100.00'
        }
        response = self.client.patch(update_url, data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.book1.refresh_from_db()
        self.assertEqual(self.book1.title, 'New Title')
        self.assertEqual(self.book1.price, 100.00)

    def test_(self):
        equal_url = reverse('book-equal')
        response = self.client.get(equal_url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_new_update(self):
        url = reverse('book-prefix')
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)