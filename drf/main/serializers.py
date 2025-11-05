from rest_framework import serializers

from .models import Book, Author, Publisher


class BookSerialzer(serializers.ModelSerializer):
    quantity = serializers.IntegerField(read_only=True)

    class Meta:
        model = Book
        fields = ["title", "author", "publisher", "price", "published_year", "quantity"]


class AuthorSerializer(serializers.ModelSerializer):
    class Meta:
        model = Author
        fields = ["name"]


class BookDiscountSerialzer(serializers.ModelSerializer):
    discount = serializers.SerializerMethodField()

    class Meta:
        model = Book
        fields = ["title", "author", "publisher", "price", "published_year", "discount"]

    def get_discount(self, obj):
        if hasattr(obj, "discount"):
            return obj.discount
        return None


class PublisherSerializer(serializers.ModelSerializer):
    books_count = serializers.IntegerField(read_only=True)
    sale_income = serializers.DecimalField(
        max_digits=12, decimal_places=2, read_only=True, allow_null=True
    )
    avg_price = serializers.DecimalField(
        max_digits=12, decimal_places=2, read_only=True, allow_null=True
    )

    class Meta:
        model = Publisher
        fields = ["name", "books_count", "sale_income", "avg_price"]


class SalesSerializer(serializers.ModelSerializer):
    month = serializers.DateField()
    total_quantity = serializers.IntegerField()

    class Meta:
        model = Book
        fields = ["title", "month", "total_quantity"]
