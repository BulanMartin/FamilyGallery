from django.db import models
from django.db.models.signals import post_delete
from django.dispatch import receiver
import os

class Group(models.Model):
    name = models.CharField(max_length=100)

    def __str__(self):
        return self.name

class Photo(models.Model):
    image = models.ImageField(upload_to='photos/')
    group = models.ForeignKey(Group, on_delete=models.CASCADE, related_name='photos')
    uploaded_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.image.name
    
# This function will be called after a Photo instance is deleted
@receiver(post_delete, sender=Photo)
def delete_image_file(sender, instance, **kwargs):
    if instance.image:
        if os.path.isfile(instance.image.path):
            os.remove(instance.image.path)