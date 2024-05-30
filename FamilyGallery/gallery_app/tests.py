from django.test import TestCase, override_settings
from django.core.files.uploadedfile import SimpleUploadedFile
from django.db.utils import IntegrityError
from .models import Group, Photo
import hashlib
import os
from time import sleep


# Override MEDIA_ROOT to a temporary directory for the tests
@override_settings(MEDIA_ROOT='/tmp/django_test_media/')
class GroupModelTest(TestCase):
    def test_group_creation(self):
        group = Group.objects.create(name="Test Group")
        self.assertEqual(group.name, "Test Group")
        self.assertEqual(str(group), "Test Group")

@override_settings(MEDIA_ROOT='/tmp/django_test_media/')
class PhotoModelTest(TestCase):
    def setUp(self):
        self.group = Group.objects.create(name="Test Group")
        self.image_file = SimpleUploadedFile("test_image.jpg", b"file_content", content_type="image/jpeg")

    def tearDown(self):
        photos = Photo.objects.all()
        for photo in photos:
            if photo.image:
                if os.path.isfile(photo.image.path):
                    os.remove(photo.image.path)
        
    def test_photo_creation(self):
        photo = Photo.objects.create(group=self.group, image=self.image_file)
        self.assertTrue(photo.image)
        self.assertEqual(photo.group, self.group)
        self.assertIsNotNone(photo.uploaded_at)
        self.assertEqual(str(photo), photo.image.name)

    def test_image_hash_calculation(self):
        photo = Photo(group=self.group, image=self.image_file)
        photo.save()
        hasher = hashlib.sha256()
        hasher.update(b"file_content")
        self.assertEqual(photo.image_hash, hasher.hexdigest())
        
    def test_duplicate_image_rejection(self):
        Photo.objects.create(group=self.group, image=self.image_file)
        with self.assertRaises(ValueError):
            duplicate_photo = Photo(group=self.group, image=self.image_file)
            duplicate_photo.save()

    def test_image_deletion(self):
        photo = Photo.objects.create(group=self.group, image=self.image_file)
        image_path = photo.image.path
        self.assertTrue(os.path.isfile(image_path))
        photo.delete()
        self.assertFalse(os.path.isfile(image_path))
        self.assertFalse(Group.objects.filter(id=self.group.id).exists())

    def test_group_not_deleted_if_photos_exist(self):
        photo1 = Photo.objects.create(group=self.group, image=self.image_file)
        image_file2 = SimpleUploadedFile("test_image2.jpg", b"file_content_2", content_type="image/jpeg")
        photo2 = Photo.objects.create(group=self.group, image=image_file2)
        photo1.delete()
        self.assertTrue(Group.objects.filter(id=self.group.id).exists())
        photo2.delete()
        self.assertFalse(Group.objects.filter(id=self.group.id).exists())

