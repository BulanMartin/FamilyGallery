from django.shortcuts import redirect, render
from .models import Photo, Group
from .forms import PhotoGroupForm

def home(request):
    return render(request, 'gallery/home.html')

def index(request):
    return render(request, 'gallery/index.html')

def gallery_view(request):
    photos = Photo.objects.all()
    return render(request, 'gallery/gallery.html', {'photos': photos})

def upload_view(request):
    if request.method == 'POST':
        title = request.POST['title']
        description = request.POST['description']
        image = request.FILES['image']
        group = Group.objects.get(id=request.POST['group'])
        Photo.objects.create(title=title, description=description, image=image, group=group)
        return redirect('gallery')
    
    groups = Group.objects.all()
    return render(request, 'gallery/upload.html', {'groups': groups})

def add_group(request):
    if request.method == 'POST':
        form = PhotoGroupForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('upload')  # Redirect to a view that lists groups, adjust as needed
    else:
        form = PhotoGroupForm()
    return render(request, 'gallery/create_group.html', {'form': form})