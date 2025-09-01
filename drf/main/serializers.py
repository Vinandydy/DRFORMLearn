from rest_framework import serializers

from .models import Book

class BookSerialzer(serializers.ModelSerializer):
    class Meta:
        model = Book
        fields = ['title', 'author', 'publisher', 'price', 'published_year']