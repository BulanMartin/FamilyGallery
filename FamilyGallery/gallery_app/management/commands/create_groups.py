from django.core.management.base import BaseCommand
from django.contrib.auth.models import Group, Permission

class Command(BaseCommand):
    help = 'Create user groups and assign permissions'

    def handle(self, *args, **kwargs):
        # Create Groups
        admin_group, created = Group.objects.get_or_create(name='admin')
        editor_group, created = Group.objects.get_or_create(name='editor')
        viewer_group, created = Group.objects.get_or_create(name='viewer')

        # Assign Permissions to Groups
        permissions = Permission.objects.filter(codename__in=['see_gallery', 'add_album', 'upload_photo', 'gallery_administration'])

        admin_group.permissions.set(permissions)  # Admins can do everything

        editor_permissions = Permission.objects.filter(codename__in=['see_gallery', 'add_album', 'upload_photo'])
        editor_group.permissions.set(editor_permissions)  

        viewer_permissions = Permission.objects.filter(codename__in=['see_gallery'])
        viewer_group.permissions.set(viewer_permissions)  # Viewers can only view

        self.stdout.write(self.style.SUCCESS('Successfully created groups and assigned permissions'))
