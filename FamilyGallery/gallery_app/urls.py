from django.urls import path
from .views import gallery_view, upload_view

urlpatterns = [
    path('', gallery_view, name='gallery'),
    path('upload/', upload_view, name='upload'),
]