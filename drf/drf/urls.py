from django.contrib import admin
from django.urls import path
from rest_framework import routers
from drf_spectacular.views import SpectacularSwaggerView, SpectacularAPIView

from main.views import BookViewSet, AuthorViewSet, PublisherViewSet

router = routers.SimpleRouter()
router.register(r"book", BookViewSet, basename="book")
router.register(r"author", AuthorViewSet, basename="author")
router.register(r"publisher", PublisherViewSet, basename="publisher")

urlpatterns = [
    path("admin/", admin.site.urls),
    path("api/schema/", SpectacularAPIView.as_view(), name="schema"),
    path("api/docs/", SpectacularSwaggerView.as_view(url_name="schema"), name="docs"),
]

urlpatterns += router.urls
