from rest_framework import serializers

from .models import Book, Author

class BookSerialzer(serializers.ModelSerializer):
    class Meta:
        model = Book
        fields = ['title', 'author', 'publisher', 'price', 'published_year']


class AuthorSerializer(serializers.ModelSerializer):
    class Meta:
        model = Author
        fields = ['name']


class BookDiscountSerialzer(serializers.ModelSerializer):
    discount = serializers.SerializerMethodField()

    class Meta:
        model = Book
        fields = ['title', 'author', 'publisher', 'price', 'published_year', 'discount']

    def get_discount(self, obj):
        if hasattr(obj, 'discount'):
            return obj.discount
        return None