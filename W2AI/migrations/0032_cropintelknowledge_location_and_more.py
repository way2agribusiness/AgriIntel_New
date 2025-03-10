# Generated by Django 4.2.2 on 2024-01-20 09:20

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('W2AI', '0031_cropintelknowledge'),
    ]

    operations = [
        migrations.AddField(
            model_name='cropintelknowledge',
            name='location',
            field=models.CharField(blank=True, max_length=1000, null=True),
        ),
        migrations.AddField(
            model_name='cropintelknowledge',
            name='season_info',
            field=models.TextField(blank=True, null=True),
        ),
        migrations.AddField(
            model_name='cropintelknowledge',
            name='spatial_distance',
            field=models.TextField(blank=True, null=True),
        ),
        migrations.AddField(
            model_name='cropintelknowledge',
            name='weather_info',
            field=models.TextField(blank=True, null=True),
        ),
        migrations.AlterField(
            model_name='cropintelknowledge',
            name='area_suitability',
            field=models.TextField(blank=True, null=True),
        ),
        migrations.AlterField(
            model_name='cropintelknowledge',
            name='irrigation_req',
            field=models.TextField(blank=True, null=True),
        ),
        migrations.AlterField(
            model_name='cropintelknowledge',
            name='market_prospects',
            field=models.TextField(blank=True, null=True),
        ),
        migrations.AlterField(
            model_name='cropintelknowledge',
            name='soil_suitability',
            field=models.TextField(blank=True, null=True),
        ),
        migrations.AlterField(
            model_name='cropintelknowledge',
            name='yield_potential',
            field=models.TextField(blank=True, null=True),
        ),
    ]
