
from django.contrib import admin
from django.urls import path
from rest_framework import routers

from main.views import BookViewSet
router = routers.SimpleRouter()
router.register(r'book', BookViewSet, basename='book')

urlpatterns = [
    path('admin/', admin.site.urls),
]

urlpatterns += router.urls
