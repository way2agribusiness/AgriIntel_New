# Generated by Django 4.2.2 on 2024-01-17 12:48

import cloudinary.models
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('W2AI', '0021_agmachinespecifications_product_image'),
    ]

    operations = [
        migrations.CreateModel(
            name='AgriFBI',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('crop', models.CharField(choices=[('Potato', 'Potato'), ('Tomato', 'Tomato'), ('Banana', 'Banana'), ('Sugarcane', 'Sugarcane'), ('Coffee', 'Coffee'), ('Pepper', 'Pepper'), ('Pappya', 'Pappya')], max_length=500)),
            ],
        ),
        migrations.CreateModel(
            name='CurrentMonthReport',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('crop', models.CharField(choices=[('Potato', 'Potato'), ('Tomato', 'Tomato'), ('Banana', 'Banana'), ('Sugarcane', 'Sugarcane'), ('Coffee', 'Coffee'), ('Pepper', 'Pepper'), ('Pappya', 'Pappya')], max_length=500)),
                ('market_price', models.FloatField()),
                ('crop_trend', cloudinary.models.CloudinaryField(max_length=255)),
                ('price_outlook', models.CharField(max_length=1000)),
                ('summary_reviews', models.TextField()),
                ('bull_bear_factors', models.TextField()),
                ('news', models.TextField()),
                ('events', models.TextField()),
                ('notifications', models.TextField()),
                ('farmer_advisor', models.TextField()),
            ],
        ),
        migrations.CreateModel(
            name='LastMonthReport',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('price_outlook', models.TextField()),
                ('bull_bear_factors', models.TextField(blank=True, null=True)),
                ('user_feedback', models.TextField()),
            ],
        ),
        migrations.CreateModel(
            name='SeasonalReport',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('price_outlook', models.TextField()),
                ('summary_reviews', models.TextField()),
                ('bull_bear_factors', models.TextField()),
            ],
        ),
        migrations.DeleteModel(
            name='CropIntel',
        ),
        migrations.AlterField(
            model_name='agmachinexuserinput',
            name='budget',
            field=models.CharField(choices=[('Below than Rs. 10000', 'Below than Rs. 10000'), ('Between Rs. 10000 to Rs. 20000', 'Between Rs. 10000 to Rs. 20000'), ('Between Rs. 20000 to Rs. 50000', 'Between Rs. 20000 to Rs. 50000'), ('Between Rs. 50000 to Rs. 1,00,000', 'Between Rs. 50000 to Rs. 1,00,000'), ('Between Rs. 1,00,000 to Rs. 1,50,000', 'Between Rs. 1,00,000 to Rs. 1,50,000'), ('Between Rs. 1,50,000 to Rs. 2,00,000', 'Between Rs. 1,50,000 to Rs. 2,00,000'), ('Between Rs. 2,00,000 to Rs. 2,50,000', 'Between Rs. 2, 00,000 to Rs. 2,50,000'), ('Above than Rs. 2,50,000', 'Above than Rs. 2,50,000')], default='', max_length=500),
        ),
    ]
