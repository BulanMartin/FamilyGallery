# Generated by Django 5.0.6 on 2024-05-29 17:51

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('gallery_app', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='photo',
            name='image_hash',
            field=models.CharField(blank=True, max_length=64, null=True, unique=True),
        ),
    ]