# Generated by Django 5.1.6 on 2025-02-10 11:01

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('W2AI', '0074_agmachinespecifications_vegetation_type_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='seocontent',
            name='keywords',
            field=models.TextField(blank=True, null=True),
        ),
    ]
