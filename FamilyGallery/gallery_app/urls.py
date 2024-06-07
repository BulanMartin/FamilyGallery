from django.urls import path
from .views import gallery_view, upload_view, add_group, gallery_administration, delete_photo, upload_folder,signup, LoginView, CustomLogoutView
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('', gallery_view, name='gallery'),
    path('upload/', upload_view, name='upload'),
    path('add-group/', add_group, name='add_group'),
    path('gallery_administration/', gallery_administration, name='gallery_administration'),
    path('delete_photo/<int:photo_id>/', delete_photo, name='delete_photo'),
    path('upload_folder/', upload_folder, name='upload_folder'),
    path('signup/', signup, name='signup'),
    path('login/', LoginView.as_view(template_name='registration/login.html'), name='login'),
    path('logout/', CustomLogoutView.as_view(), name='logout'),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)