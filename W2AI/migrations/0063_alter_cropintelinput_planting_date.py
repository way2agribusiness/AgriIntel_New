# Generated by Django 4.2.2 on 2024-07-26 04:11

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('W2AI', '0062_contact_is_seen'),
    ]

    operations = [
        migrations.AlterField(
            model_name='cropintelinput',
            name='planting_date',
            field=models.DateField(blank=True, null=True),
        ),
    ]
