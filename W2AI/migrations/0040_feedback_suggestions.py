# Generated by Django 4.2.2 on 2024-01-28 08:04

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('W2AI', '0039_remove_feedback_improvement_area_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='feedback',
            name='suggestions',
            field=models.TextField(default=''),
        ),
    ]
