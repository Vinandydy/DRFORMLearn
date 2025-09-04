from decimal import Decimal
from email.policy import default
from pickle import FALSE

from django.core.serializers import get_serializer
from django.db.models import Count, F, Q, ExpressionWrapper, DecimalField, Sum, Avg
from django.db.models.functions import TruncMonth
from django.shortcuts import render

from django.db import transaction

from rest_framework import mixins, viewsets
from rest_framework.decorators import action
from rest_framework.response import Response

from .serializers import BookSerialzer, BookDiscountSerialzer, AuthorSerializer, PublisherSerializer, SalesSerializer

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

    #Задание 8
    @action(
        detail=False,
        methods=['GET'],
        url_path='is_cheap_or_expensive'
    )
    def book_price(self, _):
        queryset = self.get_queryset().filter(Q(price__gt=2000) | Q(price__lt=500))
        serializer = self.get_serializer(queryset, many=True)

        return Response(serializer.data)

    #Задание 7
    @action(
        detail=False,
        methods=['GET'],
        url_path='prefix'
    )
    def book_prefix(self, _):
        queryset = self.get_queryset().filter(title__contains='Book:')
        serializer = self.get_serializer(queryset, many=True)

        return Response(serializer.data)

    #Задание 10.
    @action(
        detail=False,
        methods=['GET'],
        url_path='five_hundred'
    )
    def five_hundred(self, _):
        queryset = self.get_queryset().annotate(discount=ExpressionWrapper(F('price')* Decimal(0.8),
                                                                           output_field=DecimalField(max_digits=12, decimal_places=2))).filter(discount__gt=500)
        serializer = BookDiscountSerialzer(queryset, many=True)

        return Response(serializer.data)

    #Задание 2
    @action(
        detail=False,
        methods=['GET'],
        url_path='sales_income'
    )
    def sales_income(self, _):
        queryset = Book.objects.annotate(
            month=TruncMonth('salesBook__sale__date')
        ).values('title', 'month').annotate(
            total_quantity=Sum('salesBook__quantity')
        ).order_by('title', 'month')
        serializer = SalesSerializer(queryset, many=True)
        return Response(serializer.data)



class AuthorViewSet(mixins.ListModelMixin,
                    viewsets.GenericViewSet):

    def get_queryset(self):
        # Задание 3.
        return Author.objects.annotate(books_quantity=Count('books')).filter(books_quantity__gt=3)

    def get_serializer_class(self):
        return AuthorSerializer

    # Задание 9. Найти книги Автора А, которые дешевле нижней границы ИЛИ книги Автора Б дороже верхней границы.
    @action(
        detail=False,
        methods=['POST'],
        url_path='find'
    )
    def find_author_book(self, request):
        data = request.data
        print(data)
        queryset = Author.objects.filter(Q(Q(name=data.get('author_a')) & Q(books__price__lt=data.get('price_a'))) |
                                              Q(Q(name=data.get('author_b')) & Q(books__price__gt=data.get('price_b')))).prefetch_related('books')
        serializer = self.get_serializer(queryset, many=True)
        return Response(serializer.data)




class PublisherViewSet(mixins.ListModelMixin,
                       viewsets.GenericViewSet):

    def get_queryset(self):
        return Publisher.objects.filter(books__published_year__gt=2010).annotate(
            books_count=Count('books'),
            sale_income=Sum('books__salesBook__quantity', default=0) * Avg('books__price'),
            avg_price=Avg('books__price')
        ).order_by('-sale_income')

    def get_serializer_class(self):
        return PublisherSerializer