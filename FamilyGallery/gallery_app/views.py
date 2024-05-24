from django.shortcuts import render
from .models import Photo

def gallery_view(request):
    photos = Photo.objects.all()
    return render(request, 'gallery/gallery.html', {'photos': photos})

def upload_view(request):
    if request.method == 'POST':
        title = request.POST['title']
        description = request.POST['description']
        image = request.FILES['image']
        Photo.objects.create(title=title, description=description, image=image)
    return render(request, 'gallery/upload.html')