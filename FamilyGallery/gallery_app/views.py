from django.shortcuts import redirect, render, get_object_or_404
from .models import Photo, Group
from .forms import PhotoGroupForm, UploadFolderForm
from django.http import HttpResponse
import hashlib
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import login
from django.contrib.auth.views import LogoutView, LoginView


def home(request):
    return render(request, 'gallery/home.html')

def index(request):
    return render(request, 'gallery/index.html')


def gallery_view(request):
    groups = Group.objects.all()
    photos_by_group = {}
    for group in groups:
        photos_by_group[group] = Photo.objects.filter(group=group)
    
    return render(request, 'gallery/gallery.html', {
        'photos_by_group': photos_by_group
    })

def upload_view(request):

    groups = Group.objects.all()

    if request.method == 'POST':
        image = request.FILES['image']
        group = Group.objects.get(id=request.POST['group'])
        try:
            Photo.objects.create(image=image, group=group)
            return redirect('gallery')
        except ValueError as e:
            return render(request, 'gallery/upload.html', {'error': str(e), 'groups': groups})
        
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

def gallery_administration(request):
    groups = Group.objects.prefetch_related('photos').all()
    return render(request, 'gallery/gallery_administration.html', {'groups': groups})

def delete_photo(request, photo_id):
    if request.method == "POST":
        photo = get_object_or_404(Photo, id=photo_id)
        photo.delete()
        return redirect('gallery_administration')
    
def upload_folder(request):
    if request.method == 'POST':
        form = UploadFolderForm(request.POST, request.FILES)
        print(form)
        print(request.FILES)
        print(request.POST)
        print(request.FILES.getlist('images'))
        if form.is_valid():
            name = form.cleaned_data['name']
            files = request.FILES.getlist('images')
            # Create a new group
            group = Group.objects.create(name=name)

            for file in files:
                # Calculate the hash of the image
                hasher = hashlib.sha256()
                for chunk in file.chunks():
                    hasher.update(chunk)
                image_hash = hasher.hexdigest()

                # Check if a photo with the same hash already exists
                if not Photo.objects.filter(image_hash=image_hash).exists():
                    Photo.objects.create(image=file, group=group, image_hash=image_hash)
                else:
                    return HttpResponse("A photo with this content already exists.")

            return redirect('gallery') 

    else:
        form = UploadFolderForm()

    return render(request, 'gallery/upload_folder.html', {'form': form})

def signup(request):
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            return redirect('home')
    else:
        form = UserCreationForm()
    return render(request, 'registration/signup.html', {'form': form})

class CustomLogoutView(LogoutView):
    template_name = 'registration/logout.html'  # Specify the logout template

class CustomLoginView(LoginView):
    template_name = 'registration/login.html'  # Specify the login template