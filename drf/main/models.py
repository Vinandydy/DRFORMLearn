from django.db import models

class Author(models.Model):
    name = models.CharField(max_length=100)

    def __str__(self):
        return self.name

class Publisher(models.Model):
    name = models.CharField(max_length=100)

    def __str__(self):
        return self.name

class Book(models.Model):
    title = models.CharField(max_length=200)
    author = models.ForeignKey(Author, on_delete=models.CASCADE, related_name='books')
    publisher = models.ForeignKey(Publisher, on_delete=models.CASCADE, related_name='books')
    price = models.DecimalField(max_digits=6, decimal_places=2)
    published_year = models.IntegerField()

class Sale(models.Model):
    book = models.ManyToManyField(Book, through='SaleBook', related_name='sales')
    date = models.DateField()


class SaleBook(models.Model):
    sale = models.ForeignKey(Sale, on_delete=models.CASCADE, related_name='salesBook')
    book = models.ForeignKey(Book, on_delete=models.CASCADE, related_name='salesBook')
    quantity = models.IntegerField(default=1)