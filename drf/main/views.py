from decimal import Decimal
from pickle import FALSE

from django.core.serializers import get_serializer
from django.db.models import Count, F, Q
from django.shortcuts import render

from django.db import transaction

from rest_framework import mixins, viewsets
from rest_framework.decorators import action
from rest_framework.response import Response

from .serializers import BookSerialzer, AuthorSerializer

# Create your views here.
from .models import *

class BookViewSet(mixins.ListModelMixin,
                  mixins.RetrieveModelMixin,
                  mixins.UpdateModelMixin,
                  viewsets.GenericViewSet):

    def get_queryset(self):
        #Задание 1.
        return Book.objects.all().select_related('author', 'publisher')

    def get_serializer_class(self):
        return BookSerialzer

    #Задача 4.
    @action(
        detail=False,
        methods=['GET'],
        url_path='equal',
    )
    def get_equal_author_publisher(self, _):
        queryset = self.get_queryset().filter(author__name=F('publisher__name'))
        serializer = self.get_serializer(queryset, many=True)
        return Response(serializer.data)

    #Задание 5.
    @action(
        detail=True,
        methods=['GET'],
        url_path='update'
    )
    @transaction.atomic
    def atomic_update(self, request, pk=None):
        instance = self.get_object()
        query_params = request.query_params
        if query_params.get('discount'):
            instance.price = Decimal(float(instance.price) * 0.8)
            instance.save()
            instance.refresh_from_db()

        return Response(BookSerialzer(instance).data)

    @action(
        detail=False,
        methods=['GET'],
        url_path='is_cheap_or_expensive'
    )
    def book_price(self, _):
        queryset = self.get_queryset().filter(Q(price__gt=2000) | Q(price__lt=500))
        serializer = self.get_serializer(queryset, many=True)

        return Response(serializer.data)







class AuthorViewSet(mixins.ListModelMixin,
                    viewsets.GenericViewSet):

    def get_queryset(self):
        # Задание 3.
        return Author.objects.annotate(books_quantity=Count('books')).filter(books_quantity__gt=3)

    def get_serializer_class(self):
        return AuthorSerializer