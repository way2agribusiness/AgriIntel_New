from django.contrib import admin
from  .models import Contact,UserProfile,Plot,ContactNumber, Crop, Advisor, FBI,  NutriTracker, AgMachineSpecifications, AgMachineXUserInput, CurrentMonthReport, LastMonthReport, SeasonalReport, AgriFBI, FBIEnquiry, CropIntelKnowledge, CropIntelInput, Feedback, AddedServices, FundRequirement, MarketPlannerStrategy, DiseaseRecognition, ACProductNPK, SymptomRecognitionKnowledge, SymptomsRecognitionInput, Highlights, ServiceFeedback, SeoContent, Brands, Credentials,IntroTextDescription
from django.utils.safestring import mark_safe
from django.templatetags.static import static
from django.db import models
from django.forms import TextInput
from .forms import CropIntelKnowledgeForm
from django.contrib.sites.models import Site
from django.contrib import admin

# admin name "http://way2agriintel.com/admin/master-console-npcs6"

class IntroTextDescriptionAdmin(admin.ModelAdmin):
    list_display = ['Englishdescription','Kannadadescription']

class ContactNumberAdmin(admin.ModelAdmin):
    list_display = ['phone_number','Time']

class ContactAdmin(admin.ModelAdmin):
	list_display = ['name','place','phone','comments','date','is_seen']

class PlotInline(admin.StackedInline):
    model = Plot
    extra=0

class UserProfileAdmin(admin.ModelAdmin):
    inlines = [PlotInline]
    list_display = ['get_username','name','whatsapp_no','get_date_joined']

    def get_username(self, obj):
        return obj.user.username
    get_username.short_description = 'Username'

    def get_date_joined(self, obj):
        return obj.user.date_joined
    get_date_joined.short_description = 'Registration Date'

class CurrenMonthReportInline(admin.StackedInline):
    model = CurrentMonthReport
    extra = 1

class LastMonthReportInline(admin.StackedInline):
    model = LastMonthReport
    extra = 1

class SeasonalReportInline(admin.StackedInline):
    model = SeasonalReport
    extra = 1

class AgriFBIAdmin(admin.ModelAdmin):
    inlines = [CurrenMonthReportInline, LastMonthReportInline, SeasonalReportInline]
    list_display = ['crop']


class FBIEnquiryAdmin(admin.ModelAdmin):
    list_display = ['user_name', 'phone_no', 'get_crop']

    def get_crop(self, obj):
        return obj.crop
    get_crop.short_description = 'Selected Crops'


from .models import Advisor

@admin.register(Advisor)
class AdvisorAdmin(admin.ModelAdmin):
    list_display = ['full_name', 'whatsapp_no', 'crop', 'crop_area', 
                    'ph_value', 'n_value', 'p_value', 'k_value', 'crop_stage']
    search_fields = ['full_name', 'whatsapp_no', 'crop', 'village', 'district', 'state']
    list_filter = ['crop', 'crop_stage', 'district', 'state']
    ordering = ['full_name']


class ExistingUserProfileAdmin(admin.ModelAdmin):
    list_display = ['customer_name','username','password']

    def customer_name(self, obj):
        return obj.customer.name if obj.customer else ""
    
class AgMachineSpecificationsAdmin(admin.ModelAdmin):
    list_display = ['product_name', 'crop', 'land_extent', 'price', 'soil_condition', 'unit']

# class AgMachineXUserInputAdmin(admin.ModelAdmin):
#     list_display = ['machinery_req', 'full_name', 'whatsapp_no']

class AgMachineXUserInputAdmin(admin.ModelAdmin):
    list_display = [
        'full_name', 'whatsapp_no', 'email_id', 'village', 'taluk', 'district', 'state', 
        'zip_code', 'land_area', 'zone', 'soil_condition', 'labours_employed', 'crop', 
        'crop_stage', 'machinery_req', 'soil_type', 'machine_available', 'irrigation_type', 
        'water_source', 'water_availability', 'current_irrigation_method', 
        'other_current_irrigation', 'irrigation_req', 'budget', 'vegetation_type'
    ]  
    search_fields = ['full_name', 'whatsapp_no', 'email_id', 'village', 'district']
    list_filter = ['machinery_req', 'budget', 'crop_stage', 'irrigation_type']
    ordering = ['full_name']
    list_editable = ['machinery_req', 'budget']
    list_display_links = ['full_name']

class ServiceFeedbackInline(admin.StackedInline):
    model = ServiceFeedback

class FeedbackAdmin(admin.ModelAdmin):
    inlines=[ServiceFeedbackInline]
    list_display = ['name','mobile_no']

class AddedServiceAdmin(admin.ModelAdmin):
    list_display = ['name','mobile_no','service_requirement']

class CropIntelKnowlegeAdmin(admin.ModelAdmin):
	list_display = ['crop','location','selected_crop_varieties', 'area_zone']
	search_fields = ['crop','location','selected_crop_varieties','area_zone']

	form = CropIntelKnowledgeForm
	class Media:
		css = {
            'all': (static('css/admin_custom.css'),)
        }
	def save_model(self, request, obj, form, change):
		crop_variety_mapping = {
            'Amla': ['Chakaiya','NA-7','Kanchan','NA-10'],
            'Avocado': ['Fuerte','Pinkerton','Hass & Reed'],
            'Cardamom': ['Fuerte', 'Pinkerton'],
            'Cashew nut': ['V-4','V-7','Bhaskara','Ullal-1','Ullal-5'],
            'Cocoa':['Criollo','Trinitario','Forastero'],
            'Coconut':['Chowghat GD','Chowghat OD','West CT'],
            'Coffee':['Arabica','Robusta'],
            'Curry leaves':['Local Landrace Variety'],
            'Dragon fruit':['White Dragon-1','Red dragon-1'],
            'Drumstick':['PKM-1','Bhagya','Trichy-1'],
            'Grapes':['LSeedless-Thomson','Sharad','Sonaka','Red globe'],
            'Guava':['Allahabad Safeda','L 49','Arka Kiran'],
            'Jackfruit':['Varikka','Idukki Gold','Muttom Varikka'],
            'Jamoon':['Bangalore Purple','NA-7','Guthi'],
            'Lime':['Eureka','Lisbon','Meyer'],
            'Macadamia':['Macadamia Integrifolia','Macadamia Tetraphylla'],
            'Mahogany':['Forest spp'],
            'Mango':['Alphenso','Raspuri','Mallika','Totapuri','Neelam'],
            'Nutmeg':['Viswasree','Keralashree'],
            'Oil Palm':['Dura','Tenera','Pisifera'],
            'Pepper':['Panniyur-1','Subhakara','Panniyur-2','Aimpiriyan'],
            'Pomegranate':['Bhagwa','Ganesh','Mridula','Ruby'],
            'Sandalwood':['Forest spp'],
            'Sapota':['Cricket Ball','Kalipatti','DHS-1','DHS-2'],
            'Teak':['Indian Teak wood']}
		selected_crop = obj.crop
		if selected_crop in crop_variety_mapping:
			obj.selected_crop_varieties = ', '.join(crop_variety_mapping[selected_crop])
		else:
			obj.selected_crop_varieties = ''

		if form.cleaned_data.get('inter_crops'):
			obj.selected_intercrops = ', '.join(form.cleaned_data['inter_crops'])
		else:
			obj.selected_intercrops = ''

        # Ensure area_zone is a list of selected values
		if isinstance(obj.area_zone, str):
			area_zones = obj.area_zone.split(',')
		else:
			area_zones = obj.area_zone

        # Handle the selected zones to set the location
		if 'Plain-North Zone' in area_zones and 'Plain-South Zone' in area_zones:
			obj.location = 'Bidar, Gulbarga(Kalaburgi), Bijapur(Vijayapura), Yadgir, Belgaum, Bagalkot, Raichur, Dharwad, Gadag, Koppala, Haveri, Bellary,Chamarajanagar, Mysuru, Mandya, Hassan, Ramanagara, Bengaluru Rural, Kolar, Chikkaballapur, Tumkur, Chikmagalur(East), Chitradurga, Davanagere, Anantapur, Chittoor(Andhra Pradesh), Krishangiri(Tamil Nadu)'

		elif 'Plain-North Zone' in area_zones and 'Coastal Zone' in area_zones:
			obj.location = 'Bidar, Gulbarga(Kalaburgi), Bijapur(Vijayapura), Yadgir, Belgaum, Bagalkot, Raichur, Dharwad, Gadag, Koppala, Haveri, Bellary,Dakshina Kannada(Mangalore),Udupi,Uttara Kannada(West),Kasargod(Kerala)'
        
		elif 'Plain-North Zone' in area_zones and 'Western (Malenadu) Zone' in area_zones:
			obj.location = 'Bidar, Gulbarga(Kalaburgi), Bijapur(Vijayapura), Yadgir, Belgaum, Bagalkot, Raichur, Dharwad, Gadag, Koppala, Haveri, Bellary,Uttara Kannada(East), Shimoga, Chikmagalur(West), Coorg(Madikeri)(Kodagu), Wayanad(Kerala), Nilgiris(Tamil Nadu)'

		elif 'Plain-South Zone' in area_zones and 'Coastal Zone' in area_zones:
			obj.location = 'Chamarajanagar, Mysuru, Mandya, Hassan, Ramanagara, Bengaluru Rural, Kolar, Chikkaballapur, Tumkur, Chikmagalur(East), Chitradurga, Davanagere, Anantapur, Chittoor(Andhra Pradesh), Krishangiri(Tamil Nadu),Dakshina Kannada(Mangalore),Udupi,Uttara Kannada(West),Kasargod(Kerala)'
        
		elif 'Plain-South Zone' in area_zones and 'Western (Malenadu) Zone' in area_zones:
			obj.location = 'Chamarajanagar, Mysuru, Mandya, Hassan, Ramanagara, Bengaluru Rural, Kolar, Chikkaballapur, Tumkur, Chikmagalur(East), Chitradurga, Davanagere, Anantapur, Chittoor(Andhra Pradesh), Krishangiri(Tamil Nadu),Uttara Kannada(East), Shimoga, Chikmagalur(West), Coorg(Madikeri)(Kodagu), Wayanad(Kerala), Nilgiris(Tamil Nadu)'
        
		elif 'Coastal Zone' in area_zones and 'Western (Malenadu) Zone' in area_zones:
			obj.location = 'Dakshina Kannada(Mangalore),Udupi,Uttara Kannada(West),Kasargod(Kerala),Uttara Kannada(East), Shimoga, Chikmagalur(West), Coorg(Madikeri)(Kodagu), Wayanad(Kerala), Nilgiris(Tamil Nadu)'
        
		elif 'Plain-North Zone' in area_zones and 'Plain-South Zone' in area_zones and 'Coastal Zone'in area_zones:
			obj.location = 'Bidar, Gulbarga(Kalaburgi), Bijapur(Vijayapura), Yadgir, Belgaum, Bagalkot, Raichur, Dharwad, Gadag, Koppala, Haveri, Bellary,Chamarajanagar, Mysuru, Mandya, Hassan, Ramanagara, Bengaluru Rural, Kolar, Chikkaballapur, Tumkur, Chikmagalur(East), Chitradurga, Davanagere, Anantapur, Chittoor(Andhra Pradesh), Krishangiri(Tamil Nadu),Dakshina Kannada(Mangalore),Udupi,Uttara Kannada(West),Kasargod(Kerala)'
        
		elif 'Plain-North Zone' in area_zones and 'Plain-South Zone' in area_zones and 'Western (Malenadu) Zone'in area_zones:
			obj.location ='Bidar, Gulbarga(Kalaburgi), Bijapur(Vijayapura), Yadgir, Belgaum, Bagalkot, Raichur, Dharwad, Gadag, Koppala, Haveri, Bellary,Chamarajanagar, Mysuru, Mandya, Hassan, Ramanagara, Bengaluru Rural, Kolar, Chikkaballapur, Tumkur, Chikmagalur(East), Chitradurga, Davanagere, Anantapur, Chittoor(Andhra Pradesh), Krishangiri(Tamil Nadu),Uttara Kannada(East), Shimoga, Chikmagalur(West), Coorg(Madikeri)(Kodagu), Wayanad(Kerala), Nilgiris(Tamil Nadu)'

		elif 'Coastal Zone' in area_zones and 'Plain-South Zone' in area_zones and 'Western (Malenadu) Zone' in area_zones:
			obj.location = 'Dakshina Kannada(Mangalore),Udupi,Uttara Kannada(West),Kasargod(Kerala),Chamarajanagar, Mysuru, Mandya, Hassan, Ramanagara, Bengaluru Rural, Kolar, Chikkaballapur, Tumkur, Chikmagalur(East), Chitradurga, Davanagere, Anantapur, Chittoor(Andhra Pradesh), Krishangiri(Tamil Nadu),Uttara Kannada(East), Shimoga, Chikmagalur(West), Coorg(Madikeri)(Kodagu), Wayanad(Kerala), Nilgiris(Tamil Nadu)'
        
		elif 'Coastal Zone' in area_zones and 'Plain-South Zone' in area_zones and 'Western (Malenadu) Zone' in area_zones and 'Plain-North Zone' in area_zones:
			obj.location = 'Dakshina Kannada(Mangalore),Udupi,Uttara Kannada(West),Kasargod(Kerala),Chamarajanagar, Mysuru, Mandya, Hassan, Ramanagara, Bengaluru Rural, Kolar, Chikkaballapur, Tumkur, Chikmagalur(East), Chitradurga, Davanagere, Anantapur, Chittoor(Andhra Pradesh), Krishangiri(Tamil Nadu),Uttara Kannada(East), Shimoga, Chikmagalur(West), Coorg(Madikeri)(Kodagu), Wayanad(Kerala), Nilgiris(Tamil Nadu),Bidar, Gulbarga(Kalaburgi), Bijapur(Vijayapura), Yadgir, Belgaum, Bagalkot, Raichur, Dharwad, Gadag, Koppala, Haveri, Bellary'

		elif 'Plain-North Zone' in area_zones:
			obj.location = 'Bidar, Gulbarga(Kalaburgi), Bijapur(Vijayapura), Yadgir, Belgaum, Bagalkot, Raichur, Dharwad, Gadag, Koppala, Haveri, Bellary'
        
		elif 'Plain-South Zone' in area_zones:
			obj.location = 'Chamarajanagar, Mysuru, Mandya, Hassan, Ramanagara, Bengaluru Rural, Kolar, Chikkaballapur, Tumkur, Chikmagalur(East), Chitradurga, Davanagere, Anantapur, Chittoor(Andhra Pradesh), Krishangiri(Tamil Nadu)'
        
		elif 'Coastal Zone' in area_zones:
			obj.location = 'Dakshina Kannada(Mangalore),Udupi,Uttara Kannada(West),Kasargod(Kerala)'
        
		elif 'Western (Malenadu) Zone' in area_zones:
			obj.location = 'Uttara Kannada(East), Shimoga, Chikmagalur(West), Coorg(Madikeri)(Kodagu), Wayanad(Kerala), Nilgiris(Tamil Nadu)'
        
		super().save_model(request, obj, form, change)

class ACProductNPKAdmin(admin.ModelAdmin):
    list_display = ['category','product_name']


from django.contrib import admin
from .models import NutriTracker

class NutriTrackerAdmin(admin.ModelAdmin):
    fieldsets = [
        ('Your Information', {
            'fields': [
                'name',
                'whatsapp_number',
                'district',
                'taluk',
                'address',
                'extent_of_land'
            ]
        }),
        ('Plot Information', {
            'fields': [
                'plot_name',
                'crop_grown',
                'land_area',
                'crop_density'
            ]
        }),
        ('Soil Information', {
            'fields': [
                'soil_condition',
                'soil_health',
                'soil_ph',
                'water_source',
                'water_availability',
                'soil_rich_nutrients',
                'soil_avg_nutrients',
                'soil_poor_nutrients'
            ]
        }),
        ('Cultivation Information', {
            'fields': [
                'sowing_month',
                'harvesting_month',
                'irrigation_method',
                'nutrient_application_times'
            ]
        }),
        ('Soil Test Report Values', {
            'fields': [
                'nitrogen_value',
                'potassium_value',
                'phosphorous_value',
                'secondary_nutrients_value',
                'micronutrients_value',
                'organic_carbon_value'
            ]
        }),
        ('Fertilizer Purchase Details', {
            'fields': [
                'crop_fertilizer_applied',
                'crop_stage',
                'fertilizer_name',
                'nutrient_deficiency',
                'fertilizer_type',
                'manufacturer_name',
                'fertilizer_quantity',
                'fertilizer_purchase_date'
            ]
        }),
    ]

    # List view configuration
    list_display = [
        'name',
        'whatsapp_number',
        'district',
        'plot_name',
        'crop_grown',
        'land_area',
        'soil_health',
        'fertilizer_name',
        'fertilizer_purchase_date'
    ]

    # Search configuration
    search_fields = [
        'name',
        'whatsapp_number',
        'district',
        'taluk',
        'plot_name',
        'crop_grown',
        'fertilizer_name',
        'manufacturer_name'
    ]

    # Filter configuration
    list_filter = [
        'district',
        'taluk',
        'crop_grown',
        'soil_condition',
        'soil_health',
        'irrigation_method',
        'fertilizer_type'
    ]
    date_hierarchy = 'fertilizer_purchase_date'


from .models import FBI, CropDetail
class CropDetailInline(admin.TabularInline):
    model = CropDetail
    extra = 1  

class FBIAdmin(admin.ModelAdmin):
    fieldsets = [
        ('Your Information', {
            'fields': [
                'name',
                'whatsapp_number',
                'district',
                'taluk',
                'address',
                'land_extent'
            ]
        }),
        ('Agri FBI Info', {
            'fields': [
                'user_type',
            ]
        }),
    ]

    inlines = [CropDetailInline]  # Include the CropDetail inline

    # List view configuration
    list_display = [
        'name',
        'whatsapp_number',
        'district',
        'user_type',
        'land_extent',
        'get_crops'
    ]

    # Search configuration
    search_fields = [
        'name',
        'whatsapp_number',
        'district',
        'taluk',
        'crop_details__crop_name',
        'crop_details__crop_variety'
    ]

    # Filter configuration
    list_filter = [
        'user_type',
        'district',
        'taluk',
        'crop_details__crop_name'
    ]

    def get_crops(self, obj):
        """Return a comma-separated list of crops for this FBI entry"""
        return ", ".join([f"{crop.crop_name} ({crop.crop_quantity} qt)" for crop in obj.crop_details.all()])
    
    get_crops.short_description = 'Crops'

#------------------------------------------- Above is Crop Intel --------------------------------------

admin.site.register(MarketPlannerStrategy)
admin.site.register(FundRequirement)
admin.site.register(Feedback, FeedbackAdmin)
admin.site.register(AddedServices, AddedServiceAdmin)
admin.site.register(UserProfile, UserProfileAdmin) 
admin.site.register(NutriTracker, NutriTrackerAdmin)
admin.site.register(FBI, FBIAdmin)
admin.site.register(CropDetail)
admin.site.register(AgMachineSpecifications, AgMachineSpecificationsAdmin)
admin.site.register(AgMachineXUserInput,AgMachineXUserInputAdmin)
admin.site.register(AgriFBI, AgriFBIAdmin)
admin.site.register(FBIEnquiry, FBIEnquiryAdmin)
admin.site.register(CropIntelKnowledge, CropIntelKnowlegeAdmin)
admin.site.register(CropIntelInput)
admin.site.register(DiseaseRecognition)
admin.site.register(ACProductNPK, ACProductNPKAdmin)
admin.site.register(SymptomRecognitionKnowledge)
admin.site.register(SymptomsRecognitionInput)
admin.site.register(Highlights)
admin.site.register(Contact,ContactAdmin)
admin.site.register(SeoContent)
admin.site.register(Brands)
admin.site.register(Credentials)
admin.site.register(IntroTextDescription,IntroTextDescriptionAdmin)
admin.site.register(ContactNumber,ContactNumberAdmin)
