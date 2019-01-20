from django.urls import path

from .views import show_inspiration_qr

urlpatterns = [
    path('<show_id>/qr/inspiration', show_inspiration_qr, name='show_inspiration_qr'),
]
