# Generated by Django 4.2.2 on 2024-05-04 12:13

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('W2AI', '0042_atscontactinfo_atsinfo_atsintro_atsseller_and_more'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='userprofile',
            name='city',
        ),
        migrations.RemoveField(
            model_name='userprofile',
            name='crop_density',
        ),
        migrations.RemoveField(
            model_name='userprofile',
            name='crops',
        ),
        migrations.RemoveField(
            model_name='userprofile',
            name='land_area',
        ),
        migrations.RemoveField(
            model_name='userprofile',
            name='plot_name1',
        ),
        migrations.RemoveField(
            model_name='userprofile',
            name='plot_name2',
        ),
        migrations.RemoveField(
            model_name='userprofile',
            name='plot_name3',
        ),
        migrations.RemoveField(
            model_name='userprofile',
            name='plot_name4',
        ),
        migrations.RemoveField(
            model_name='userprofile',
            name='plot_name5',
        ),
        migrations.AddField(
            model_name='userprofile',
            name='village',
            field=models.CharField(default='', max_length=500),
        ),
        migrations.AddField(
            model_name='userprofile',
            name='zip_code',
            field=models.CharField(default='', max_length=6),
        ),
        migrations.AddField(
            model_name='userprofile',
            name='zone',
            field=models.CharField(blank=True, max_length=500, null=True),
        ),
        migrations.AlterField(
            model_name='userprofile',
            name='district',
            field=models.CharField(blank=True, max_length=500, null=True),
        ),
        migrations.AlterField(
            model_name='userprofile',
            name='state',
            field=models.CharField(blank=True, max_length=255, null=True),
        ),
        migrations.CreateModel(
            name='Plot',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('plot_name', models.CharField(blank=True, max_length=500, null=True)),
                ('crop_grown', models.CharField(blank=True, choices=[('Amla', 'Amla'), ('Areca New', 'Areca New'), ('Avocado', 'Avocado'), ('Arecanut', 'Arecanut'), ('Banana', 'Banana'), ('Betelvine', 'Betelvine'), ('Carrot', 'Carrot'), ('Cashewnut', 'Cashewnut'), ('Cauliflower (Cole Crops)', 'Cauliflower (Cole Crops)'), ('Chilli', 'Chilli'), ('Chrysanthemum', 'Chrysanthemum'), ('Citrus', 'Citrus'), ('Cocoa', 'Cocoa'), ('Coconut', 'Coconut'), ('Coffee', 'Coffee'), ('Cotton', 'Cotton'), ('Curry Leaves', 'Curry Leaves'), ('Custard Apple', 'Custard Apple'), ('Dragon Fruit', 'Dragon Fruit'), ('Drumstick', 'Drumstick'), ('Durian', 'Durian'), ('Fig', 'Fig'), ('Ginger', 'Ginger'), ('Grapes', 'Grapes'), ('Groundnut', 'Groundnut'), ('Guava', 'Guava'), ('Jack Fruit', 'Jack Fruit'), ('Jasmin', 'Jasmin'), ('Kokum', 'Kokum'), ('Lime', 'Lime'), ('Macadamia', 'Macadamia'), ('Mahogani', 'Mahogani'), ('Maize', 'Maize'), ('Mango', 'Mango'), ('Mangosteen', 'Mangosteen'), ('Mosambi', 'Mosambi'), ('Nutmeg', 'Nutmeg'), ('Onion', 'Onion'), ('Paddy', 'Paddy'), ('Papaya', 'Papaya'), ('Pepper', 'Pepper'), ('Pineapple', 'Pine apple'), ('Pomegranate', 'Pomegranate'), ('Potato', 'Potato'), ('Rambutan', 'Rambutan'), ('Rose', 'Rose'), ('Rosewood', 'Rosewood'), ('Sapota', 'Sapota'), ('Sugarcane', 'Sugarcane'), ('Tender Coconut', 'Tender Coconut'), ('Tomato', 'Tomato'), ('Tur', 'Tur'), ('Turmeric', 'Turmeric')], max_length=500, null=True)),
                ('land_area', models.CharField(blank=True, max_length=100, null=True)),
                ('soil_condition', models.CharField(blank=True, choices=[('Soft', 'Soft'), ('Hard', 'Hard'), ('With Stone', 'With Stone')], max_length=255, null=True)),
                ('soil_health', models.CharField(blank=True, choices=[('Good', 'Good'), ('Average', 'Average'), ('Poor', 'Poor')], max_length=255, null=True)),
                ('soil_ph', models.CharField(blank=True, choices=[('Less than 6.5 (Acidic)', 'Less than 6.5(Acidic)'), ('6.5 - 7.5 (Neutral)', '6.5 - 7.5 (Neutral)'), ('Higher than 7.5 (Alkaline)', 'Higher than 7.5 (Alkaline)')], max_length=255, null=True)),
                ('soil_rich_nutrients', models.CharField(blank=True, choices=[('Organic Matter', 'Organic Matter'), ('Nitrogen (N)', 'Nitrogen (N)'), ('Phosphorus (P)', 'Phosphorus (P)'), ('Potassium (K)', 'Potassium (K)'), ('Calcium (Ca)', 'Calcium (Ca)'), ('Magnesium (Mg)', 'Magnesium (Mg)'), ('Sulphur(S)', 'Sulphur(S)'), ('Iron (Fe)', 'Iron (Fe)'), ('Manganese (Mn)', 'Manganese (Mn)'), ('Zinc (Zn)', 'Zinc (Zn)'), ('Copper (Cu)', 'Copper (Cu)'), ('Boron (B)', 'Boron (B)'), ('Molybdenum (Mo)', 'Molybdenum (Mo)')], max_length=255, null=True)),
                ('soil_average_nutrients', models.CharField(blank=True, choices=[('Organic Matter', 'Organic Matter'), ('Nitrogen (N)', 'Nitrogen (N)'), ('Phosphorus (P)', 'Phosphorus (P)'), ('Potassium (K)', 'Potassium (K)'), ('Calcium (Ca)', 'Calcium (Ca)'), ('Magnesium (Mg)', 'Magnesium (Mg)'), ('Sulphur(S)', 'Sulphur(S)'), ('Iron (Fe)', 'Iron (Fe)'), ('Manganese (Mn)', 'Manganese (Mn)'), ('Zinc (Zn)', 'Zinc (Zn)'), ('Copper (Cu)', 'Copper (Cu)'), ('Boron (B)', 'Boron (B)'), ('Molybdenum (Mo)', 'Molybdenum (Mo)')], max_length=255, null=True)),
                ('soil_poor_nutrients', models.CharField(blank=True, choices=[('Organic Matter', 'Organic Matter'), ('Nitrogen (N)', 'Nitrogen (N)'), ('Phosphorus (P)', 'Phosphorus (P)'), ('Potassium (K)', 'Potassium (K)'), ('Calcium (Ca)', 'Calcium (Ca)'), ('Magnesium (Mg)', 'Magnesium (Mg)'), ('Sulphur(S)', 'Sulphur(S)'), ('Iron (Fe)', 'Iron (Fe)'), ('Manganese (Mn)', 'Manganese (Mn)'), ('Zinc (Zn)', 'Zinc (Zn)'), ('Copper (Cu)', 'Copper (Cu)'), ('Boron (B)', 'Boron (B)'), ('Molybdenum (Mo)', 'Molybdenum (Mo)')], max_length=255, null=True)),
                ('water_source', models.CharField(blank=True, choices=[('Rain Fed', 'Rain Fed'), ('Borewell', 'Borewell'), ('Others', 'Others')], max_length=255, null=True)),
                ('water_availability', models.CharField(blank=True, choices=[('Good Water Availability', 'Good Water Availability'), ('Average Water Availability', 'Average Water Availability'), ('Limited Water Availability', 'Limited Water Availability')], max_length=255, null=True)),
                ('user_profile', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='W2AI.userprofile')),
            ],
        ),
    ]
