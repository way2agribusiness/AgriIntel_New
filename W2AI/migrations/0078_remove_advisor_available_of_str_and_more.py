# Generated by Django 5.1.6 on 2025-02-18 06:42

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('W2AI', '0077_delete_contact_number_alter_advisor_crop_and_more'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='advisor',
            name='available_of_str',
        ),
        migrations.RemoveField(
            model_name='advisor',
            name='nitrogen',
        ),
        migrations.RemoveField(
            model_name='advisor',
            name='phosphorus',
        ),
        migrations.RemoveField(
            model_name='advisor',
            name='potassium',
        ),
    ]
