from django.shortcuts import render

from rest_framework import mixins, viewsets

from .serializers import BookSerialzer

# Create your views here.
from .models import *

class BookViewSet(mixins.ListModelMixin,
                  viewsets.GenericViewSet):

    def get_queryset(self):
        return Book.objects.all()

    def get_serializer_class(self):
        return BookSerialzer