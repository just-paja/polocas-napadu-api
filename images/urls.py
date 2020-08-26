from django.urls import path

from .views import thumbnail

urlpatterns = [
    path("thumb/<image_size>/<image_format>", thumbnail, name="thumb"),
]
