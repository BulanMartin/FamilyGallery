from django.contrib import admin
from .models import Photo, Group

@admin.register(Group)
class GroupAdmin(admin.ModelAdmin):
    list_display = ['id', 'name']

@admin.register(Photo)
class PhotoAdmin(admin.ModelAdmin):
    list_display = ['id', 'group', 'image', 'image_hash']
    list_filter = ['group']

#admin.site.register(Photo)
#admin.site.register(Group)
# Register your models here.
