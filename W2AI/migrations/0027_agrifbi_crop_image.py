# Generated by Django 4.2.2 on 2024-01-18 11:14

import cloudinary.models
from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('W2AI', '0026_alter_agrifbi_crop'),
    ]

    operations = [
        migrations.AddField(
            model_name='agrifbi',
            name='crop_image',
            field=cloudinary.models.CloudinaryField(default='', max_length=255),
        ),
    ]
