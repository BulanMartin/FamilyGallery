from django.db import models
from django.db.models.signals import post_delete
from django.dispatch import receiver
import os, hashlib


class Group(models.Model):
    name = models.CharField(max_length=100)

    def __str__(self):
        return self.name

class Photo(models.Model):
    image = models.ImageField(upload_to='photos/')
    group = models.ForeignKey(Group, on_delete=models.CASCADE, related_name='photos')
    image_hash = models.CharField(max_length=64, unique=True, blank=True, null=True)
    uploaded_at = models.DateTimeField(auto_now_add=True)

    def save(self, *args, **kwargs):
        if not self.image_hash:
            # Calculate the hash of the image
            self.image_hash = self.calculate_hash()
            
        # Check if a photo with the same hash already exists
        if Photo.objects.filter(image_hash=self.image_hash).exists():
            raise ValueError("A photo with this content already exists.")
            
        super().save(*args, **kwargs)

    def calculate_hash(self):
        hasher = hashlib.sha256()
        for chunk in self.image.chunks():
            hasher.update(chunk)
        return hasher.hexdigest()

    def __str__(self):
        return self.image.name
    
# This function will be called after a Photo instance is deleted
@receiver(post_delete, sender=Photo)
def delete_image_file(sender, instance, **kwargs):
    if instance.image:
        if os.path.isfile(instance.image.path):
            os.remove(instance.image.path)