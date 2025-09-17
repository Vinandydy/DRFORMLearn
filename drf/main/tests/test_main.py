from main.models import *
from rest_framework.test import APITestCase
from rest_framework import status
from django.urls import reverse

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

    title = factory.Faker('sentence')
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
