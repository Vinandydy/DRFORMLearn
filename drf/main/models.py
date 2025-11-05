from django.db import models


class Author(models.Model):
    name: models.CharField = models.CharField(max_length=100)

    def __str__(self) -> str:
        return self.name


class Publisher(models.Model):
    name: models.CharField = models.CharField(max_length=100)

    def __str__(self) -> str:
        return self.name


class Book(models.Model):
    title: models.CharField = models.CharField(max_length=200)
    author: models.ForeignKey = models.ForeignKey(
        Author, on_delete=models.CASCADE, related_name="books"
    )
    publisher: models.ForeignKey = models.ForeignKey(
        Publisher, on_delete=models.CASCADE, related_name="books"
    )
    price: models.DecimalField = models.DecimalField(max_digits=6, decimal_places=2)
    published_year: models.IntegerField = models.IntegerField()


class Sale(models.Model):
    book: models.ManyToManyField = models.ManyToManyField(
        Book, through="SaleBook", related_name="sales"
    )
    date: models.DateField = models.DateField()


class SaleBook(models.Model):
    sale: models.ForeignKey = models.ForeignKey(
        Sale, on_delete=models.CASCADE, related_name="salesBook"
    )
    book: models.ForeignKey = models.ForeignKey(
        Book, on_delete=models.CASCADE, related_name="salesBook"
    )
    quantity: models.IntegerField = models.IntegerField(default=1)
