import random
from django.core.management.base import BaseCommand
from django.db import transaction
from faker import Faker
from main.models import Author, Publisher, Book, Sale

class Command(BaseCommand):

    def add_arguments(self, parser):
        parser.add_argument('--authors', type=int, default=100, help='Number of authors to create')
        parser.add_argument('--publishers', type=int, default=50, help='Number of publishers to create')
        parser.add_argument('--books', type=int, default=1000, help='Number of books to create')
        parser.add_argument('--sales', type=int, default=5000, help='Number of sales to create')

    def handle(self, *args, **options):
        fake = Faker()
        num_authors = options['authors']
        num_publishers = options['publishers']
        num_books = options['books']
        num_sales = options['sales']

        self.stdout.write(self.style.SUCCESS('Starting database population...'))

        with transaction.atomic():
            authors = [Author(name=fake.name()) for _ in range(num_authors)]
            Author.objects.bulk_create(authors)
            self.stdout.write(self.style.SUCCESS(f'Created {num_authors} authors.'))

            publishers = [Publisher(name=fake.company()) for _ in range(num_publishers)]
            Publisher.objects.bulk_create(publishers)
            self.stdout.write(self.style.SUCCESS(f'Created {num_publishers} publishers.'))

            books = []
            for _ in range(num_books):
                book = Book(
                    title=fake.sentence(nb_words=4),
                    author=random.choice(authors),
                    publisher=random.choice(publishers),
                    price=random.uniform(10.0, 100.0),
                    published_year=random.randint(1900, 2025)
                )
                books.append(book)
            Book.objects.bulk_create(books)
            self.stdout.write(self.style.SUCCESS(f'Created {num_books} books.'))

            sales = []
            for _ in range(num_sales):
                sale = Sale(
                    book=random.choice(books),
                    quantity=random.randint(1, 100),
                    date=fake.date_between(start_date='-5y', end_date='today')
                )
                sales.append(sale)
            Sale.objects.bulk_create(sales)
            self.stdout.write(self.style.SUCCESS(f'Created {num_sales} sales.'))

        self.stdout.write(self.style.SUCCESS('Database population completed!'))