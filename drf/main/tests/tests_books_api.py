from rest_framework.test import APITestCase
from rest_framework import status
from django.urls import reverse

from main.models import *

import factory

class AuthorFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = Author

    name = factory.Faker('name')


class PublisherFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = Publisher

    name = factory.Faker('company')


class BookFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = Book

    title = factory.Faker('sentence', nb_words=3)
    author = factory.SubFactory(AuthorFactory)
    publisher = factory.SubFactory(PublisherFactory)
    price = factory.Faker('pydecimal', positive=True)
    published_year = factory.Faker('year')


class SaleFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = Sale

    date = factory.Faker('date_this_decade')

class SaleBookFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = SaleBook

    sale = factory.SubFactory(SaleFactory)
    book = factory.SubFactory(BookFactory)
    quantity = factory.Faker('random_int', min=1, max=100)


class BookAPITest(APITestCase):
    def setUp(self):
        self.book1 = BookFactory
        self.book2 = BookFactory
        self.book_url = reverse('book-list')

    def test_create_book(self):
        author = AuthorFactory()
        publisher = PublisherFactory()
        data = {
            'title': "Test 1",
            'author': author.id,
            'publisher': publisher.id,
            'price': '100.00',
            'published_year': 2020
        }
        response = self.client.post(self.book_url, data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Book.objects.count(), 3)