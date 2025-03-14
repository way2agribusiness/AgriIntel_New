# Generated by Django 4.2.2 on 2023-12-23 08:03

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('W2AI', '0005_brands_contact_credentials_crop_advisor'),
    ]

    operations = [
        migrations.CreateModel(
            name='NewFarmerPurchaseHistory',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=255)),
                ('whatsapp_no', models.CharField(max_length=255)),
                ('email', models.CharField(blank=True, max_length=255, null=True)),
                ('fertilizer1', models.CharField(max_length=500)),
                ('quantity1', models.CharField(max_length=10)),
                ('purchase_date1', models.DateField()),
                ('fertilizer2', models.CharField(blank=True, max_length=500, null=True)),
                ('quantity2', models.CharField(blank=True, max_length=10, null=True)),
                ('purchase_date2', models.DateField(blank=True, null=True)),
                ('fertilizer3', models.CharField(blank=True, max_length=500, null=True)),
                ('quantity3', models.CharField(blank=True, max_length=10, null=True)),
                ('purchase_date3', models.DateField(blank=True, null=True)),
                ('fertilizer4', models.CharField(blank=True, max_length=500, null=True)),
                ('quantity4', models.CharField(blank=True, max_length=10, null=True)),
                ('purchase_date4', models.DateField(blank=True, null=True)),
                ('fertilizer5', models.CharField(blank=True, max_length=500, null=True)),
                ('quantity5', models.CharField(blank=True, max_length=10, null=True)),
                ('purchase_date5', models.DateField(blank=True, null=True)),
            ],
            options={
                'ordering': ['-purchase_date1', '-purchase_date2', '-purchase_date3', '-purchase_date4', '-purchase_date5'],
            },
        ),
    ]
