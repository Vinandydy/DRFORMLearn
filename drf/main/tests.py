from django.test import TestCase

# Create your tests here.

class TestBook(TestCase):

    def test_book(self):
        response = self.client.get('/book/')
        self.assertEqual(response.status_code, 200)

    def test_equal(self):
        response = self.client.get('/book/equal/')
        self.assertEqual(response.status_code, 200)