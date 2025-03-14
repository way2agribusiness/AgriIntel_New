# Generated by Django 4.2.2 on 2024-01-20 12:27

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('W2AI', '0032_cropintelknowledge_location_and_more'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='cropintelknowledge',
            options={'verbose_name': 'CropIntel KnowledgeBase', 'verbose_name_plural': 'CropIntel KnowledgeBase'},
        ),
        migrations.CreateModel(
            name='CropIntelInput',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('soil_test_report', models.TextField()),
                ('land_type', models.CharField(choices=[('New Land', 'New Land'), ('Existing Land', 'Existing Land')], max_length=500)),
                ('crop_stage', models.CharField(max_length=500)),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='W2AI.userprofile')),
            ],
            options={
                'verbose_name': 'CropIntel User Input',
                'verbose_name_plural': 'CropIntel User Input',
            },
        ),
    ]
