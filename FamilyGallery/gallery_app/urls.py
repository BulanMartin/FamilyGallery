from django.urls import path
from .views import gallery_view, upload_view, add_group


urlpatterns = [
    path('', gallery_view, name='gallery'),
    path('upload/', upload_view, name='upload'),
    path('add-group/', add_group, name='add_group'),
]