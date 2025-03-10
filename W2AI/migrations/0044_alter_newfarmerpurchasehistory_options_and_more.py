# Generated by Django 4.2.2 on 2024-05-04 12:20

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('W2AI', '0043_remove_userprofile_city_and_more'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='newfarmerpurchasehistory',
            options={},
        ),
        migrations.RemoveField(
            model_name='newfarmerpurchasehistory',
            name='city',
        ),
        migrations.RemoveField(
            model_name='newfarmerpurchasehistory',
            name='fertilizer1',
        ),
        migrations.RemoveField(
            model_name='newfarmerpurchasehistory',
            name='fertilizer2',
        ),
        migrations.RemoveField(
            model_name='newfarmerpurchasehistory',
            name='fertilizer3',
        ),
        migrations.RemoveField(
            model_name='newfarmerpurchasehistory',
            name='fertilizer4',
        ),
        migrations.RemoveField(
            model_name='newfarmerpurchasehistory',
            name='fertilizer5',
        ),
        migrations.RemoveField(
            model_name='newfarmerpurchasehistory',
            name='plot_name1',
        ),
        migrations.RemoveField(
            model_name='newfarmerpurchasehistory',
            name='plot_name2',
        ),
        migrations.RemoveField(
            model_name='newfarmerpurchasehistory',
            name='plot_name3',
        ),
        migrations.RemoveField(
            model_name='newfarmerpurchasehistory',
            name='plot_name4',
        ),
        migrations.RemoveField(
            model_name='newfarmerpurchasehistory',
            name='plot_name5',
        ),
        migrations.RemoveField(
            model_name='newfarmerpurchasehistory',
            name='purchase_date1',
        ),
        migrations.RemoveField(
            model_name='newfarmerpurchasehistory',
            name='purchase_date2',
        ),
        migrations.RemoveField(
            model_name='newfarmerpurchasehistory',
            name='purchase_date3',
        ),
        migrations.RemoveField(
            model_name='newfarmerpurchasehistory',
            name='purchase_date4',
        ),
        migrations.RemoveField(
            model_name='newfarmerpurchasehistory',
            name='purchase_date5',
        ),
        migrations.RemoveField(
            model_name='newfarmerpurchasehistory',
            name='quantity1',
        ),
        migrations.RemoveField(
            model_name='newfarmerpurchasehistory',
            name='quantity2',
        ),
        migrations.RemoveField(
            model_name='newfarmerpurchasehistory',
            name='quantity3',
        ),
        migrations.RemoveField(
            model_name='newfarmerpurchasehistory',
            name='quantity4',
        ),
        migrations.RemoveField(
            model_name='newfarmerpurchasehistory',
            name='quantity5',
        ),
        migrations.AddField(
            model_name='newfarmerpurchasehistory',
            name='crop_grown',
            field=models.CharField(blank=True, max_length=500, null=True),
        ),
        migrations.AddField(
            model_name='newfarmerpurchasehistory',
            name='harvesting_month',
            field=models.CharField(blank=True, choices=[('January', 'January'), ('February', 'February'), ('March', 'March'), ('April', 'April'), ('May', 'May'), ('June', 'June'), ('July', 'July'), ('August', 'August'), ('September', 'September'), ('October', 'October'), ('November', 'November'), ('December', 'December')], max_length=255, null=True),
        ),
        migrations.AddField(
            model_name='newfarmerpurchasehistory',
            name='irrigation_method',
            field=models.CharField(blank=True, choices=[('Flood Irrigation', 'Flood Irrigation'), ('Sprinkler Irrigation', 'Sprinkler Irrigation'), ('Drip Irrigation', 'Drip Irrigation'), ('Other Irrigation Method', 'Other Irrigation Method')], max_length=500, null=True),
        ),
        migrations.AddField(
            model_name='newfarmerpurchasehistory',
            name='micro_nutrients',
            field=models.CharField(blank=True, max_length=255, null=True),
        ),
        migrations.AddField(
            model_name='newfarmerpurchasehistory',
            name='nitrogen',
            field=models.CharField(blank=True, max_length=255, null=True),
        ),
        migrations.AddField(
            model_name='newfarmerpurchasehistory',
            name='nutrients_freq',
            field=models.IntegerField(blank=True, default=0, null=True),
        ),
        migrations.AddField(
            model_name='newfarmerpurchasehistory',
            name='organic_carbon',
            field=models.CharField(blank=True, max_length=500, null=True),
        ),
        migrations.AddField(
            model_name='newfarmerpurchasehistory',
            name='other_irrigation',
            field=models.CharField(blank=True, max_length=500, null=True),
        ),
        migrations.AddField(
            model_name='newfarmerpurchasehistory',
            name='phosphorous',
            field=models.CharField(blank=True, max_length=255, null=True),
        ),
        migrations.AddField(
            model_name='newfarmerpurchasehistory',
            name='planting_month',
            field=models.CharField(blank=True, choices=[('January', 'January'), ('February', 'February'), ('March', 'March'), ('April', 'April'), ('May', 'May'), ('June', 'June'), ('July', 'July'), ('August', 'August'), ('September', 'September'), ('October', 'October'), ('November', 'November'), ('December', 'December')], max_length=255, null=True),
        ),
        migrations.AddField(
            model_name='newfarmerpurchasehistory',
            name='plot_name',
            field=models.CharField(blank=True, max_length=500, null=True),
        ),
        migrations.AddField(
            model_name='newfarmerpurchasehistory',
            name='potassium',
            field=models.CharField(blank=True, max_length=255),
        ),
        migrations.AddField(
            model_name='newfarmerpurchasehistory',
            name='secondary_nutrients',
            field=models.CharField(blank=True, max_length=255, null=True),
        ),
        migrations.AddField(
            model_name='newfarmerpurchasehistory',
            name='soil_average_nutrients',
            field=models.CharField(blank=True, max_length=255, null=True),
        ),
        migrations.AddField(
            model_name='newfarmerpurchasehistory',
            name='soil_condition',
            field=models.CharField(blank=True, max_length=255, null=True),
        ),
        migrations.AddField(
            model_name='newfarmerpurchasehistory',
            name='soil_health',
            field=models.CharField(blank=True, max_length=255, null=True),
        ),
        migrations.AddField(
            model_name='newfarmerpurchasehistory',
            name='soil_ph',
            field=models.CharField(blank=True, max_length=255, null=True),
        ),
        migrations.AddField(
            model_name='newfarmerpurchasehistory',
            name='soil_poor_nutrients',
            field=models.CharField(blank=True, max_length=255, null=True),
        ),
        migrations.AddField(
            model_name='newfarmerpurchasehistory',
            name='soil_rich_nutrients',
            field=models.CharField(blank=True, max_length=255, null=True),
        ),
        migrations.AddField(
            model_name='newfarmerpurchasehistory',
            name='water_availability',
            field=models.CharField(blank=True, max_length=255, null=True),
        ),
        migrations.AddField(
            model_name='newfarmerpurchasehistory',
            name='water_source',
            field=models.CharField(blank=True, max_length=255, null=True),
        ),
        migrations.AlterField(
            model_name='newfarmerpurchasehistory',
            name='crop_density',
            field=models.CharField(blank=True, max_length=255, null=True),
        ),
        migrations.AlterField(
            model_name='newfarmerpurchasehistory',
            name='district',
            field=models.CharField(blank=True, max_length=500, null=True),
        ),
        migrations.AlterField(
            model_name='newfarmerpurchasehistory',
            name='state',
            field=models.CharField(default='', max_length=255),
        ),
        migrations.AlterField(
            model_name='newfarmerpurchasehistory',
            name='taluk',
            field=models.CharField(blank=True, max_length=500, null=True),
        ),
        migrations.CreateModel(
            name='NTFertilizerPurchase',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('crop', models.CharField(choices=[('Amla', 'Amla'), ('Areca New', 'Areca New'), ('Avocado', 'Avocado'), ('Arecanut', 'Arecanut'), ('Banana', 'Banana'), ('Betelvine', 'Betelvine'), ('Carrot', 'Carrot'), ('Cashewnut', 'Cashewnut'), ('Cauliflower (Cole Crops)', 'Cauliflower (Cole Crops)'), ('Chilli', 'Chilli'), ('Chrysanthemum', 'Chrysanthemum'), ('Citrus', 'Citrus'), ('Cocoa', 'Cocoa'), ('Coconut', 'Coconut'), ('Coffee', 'Coffee'), ('Cotton', 'Cotton'), ('Curry Leaves', 'Curry Leaves'), ('Custard Apple', 'Custard Apple'), ('Dragon Fruit', 'Dragon Fruit'), ('Drumstick', 'Drumstick'), ('Durian', 'Durian'), ('Fig', 'Fig'), ('Ginger', 'Ginger'), ('Grapes', 'Grapes'), ('Groundnut', 'Groundnut'), ('Guava', 'Guava'), ('Jack Fruit', 'Jack Fruit'), ('Jasmin', 'Jasmin'), ('Kokum', 'Kokum'), ('Lime', 'Lime'), ('Macadamia', 'Macadamia'), ('Mahogani', 'Mahogani'), ('Maize', 'Maize'), ('Mango', 'Mango'), ('Mangosteen', 'Mangosteen'), ('Mosambi', 'Mosambi'), ('Nutmeg', 'Nutmeg'), ('Onion', 'Onion'), ('Paddy', 'Paddy'), ('Papaya', 'Papaya'), ('Pepper', 'Pepper'), ('Pineapple', 'Pine apple'), ('Pomegranate', 'Pomegranate'), ('Potato', 'Potato'), ('Rambutan', 'Rambutan'), ('Rose', 'Rose'), ('Rosewood', 'Rosewood'), ('Sapota', 'Sapota'), ('Sugarcane', 'Sugarcane'), ('Tender Coconut', 'Tender Coconut'), ('Tomato', 'Tomato'), ('Tur', 'Tur'), ('Turmeric', 'Turmeric')], max_length=100)),
                ('crop_stage', models.CharField(choices=[('Early Stage', 'Early Stage'), ('Vegetative Stage', 'Vegetative Stage'), ('Yielding Stage', 'Yielding Stage')], max_length=256)),
                ('fertilizer', models.CharField(max_length=500)),
                ('nutrients', models.CharField(choices=[('Nitrogen', 'Nitrogen'), ('Potassium', 'Potassium'), ('Phosphorous', 'Phosphorous'), ('Calcium', 'Calcium'), ('Magenesium', 'Magenesium'), ('Manganese', 'Manganese'), ('Copper', 'Copper'), ('Zinc', 'Zinc'), ('Sulphur', 'Sulphur'), ('Boron', 'Boron'), ('Iron', 'Iron'), ('Molybdenum', 'Molybdenum')], max_length=500)),
                ('fertilizer_type', models.CharField(choices=[('Organic Fertilizer', 'Organic Fertilizer'), ('Inorganic Fertilizer', 'Inorganic Fertilizer'), ('FYM', 'FYM')], max_length=500)),
                ('brand', models.CharField(max_length=500)),
                ('quantity', models.CharField(max_length=10)),
                ('purchase_date', models.DateField()),
                ('new_user_info', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='W2AI.newfarmerpurchasehistory')),
            ],
            options={
                'verbose_name': 'NT New User Purchase Info',
                'verbose_name_plural': 'NT New User Purchase Info',
            },
        ),
    ]
