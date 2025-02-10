from django.contrib import admin
from  .models import Contact,UserProfile,Plot, NewFarmerPurchaseHistory,ContactNumber, Crop, Advisor, ProductPurchased, NutriTracker,ExistingUserProfile, AgMachineSpecifications, AgMachineXUserInput, CurrentMonthReport, LastMonthReport, SeasonalReport, AgriFBI, FBIEnquiry, CropIntelKnowledge, CropIntelInput, NutriTrackerSchedule, Feedback, AddedServices, FundRequirement, MarketPlannerStrategy, DiseaseRecognition, ACProductNPK, SymptomRecognitionKnowledge, SymptomsRecognitionInput, Highlights, ATSInfo, ATSContactInfo,ATSContactProductInfo,ATSContactProductImages,ATSIntro,ATSSeller, ATSSellerProductImage, ATSRoadmap, ServiceFeedback, SeoContent, Brands, Credentials,NotificationRecord,IntroTextDescription
from django.utils.safestring import mark_safe
from django.templatetags.static import static
from django.db import models
from django.forms import TextInput
from .forms import CropIntelKnowledgeForm
from django.contrib.sites.models import Site


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

class ProductPurchasedInline(admin.TabularInline):
    model = ProductPurchased
    extra = 1
    formfield_overrides = {
        models.CharField: {'widget': TextInput(attrs={'size':'30'})},
    }

class NutriTrackerAdmin(admin.ModelAdmin):
    inlines = [ProductPurchasedInline]
    list_display = ['name','whatsapp_no','product_purchase_info']

    def product_purchase_info(self, obj):
        products = ProductPurchased.objects.filter(customer=obj)
        product_dict = {}
        for product in products:
            if product.date:
                formatted_date = product.date.strftime('%d-%m-%Y')
                if formatted_date in product_dict:
                    product_dict[formatted_date].append((product.product_name, product.quantity))
                else:
                    product_dict[formatted_date] = [(product.product_name, product.quantity)]
            else:
                formatted_date = 'No Date'
        table = '<table>'
        for date, products in product_dict.items():
            product_rows = ''.join(f"<tr style='display:flex; justify-content: space-between; width: 80%;'><td>{product[0]}</td><td>{product[1]}</td></tr>" for product in products)
            table += f"<tr><td><strong style='font-family:times new roman; font-size:15px'>{date}</strong></td><td>{product_rows}</td></tr>"
        table += '</table>'
        return mark_safe(table) if table != '<table></table>' else '-'
    product_purchase_info.short_description = 'Purchase-Info'   

class NewFarmerPurchaseHistoryAdmin(admin.ModelAdmin):
    list_display = ['name','whatsapp_no','get_email','purchase_info']

    def get_email(self, obj):
        if obj.email:
            return obj.email
        else:
            return ''
    get_email.short_description = 'Email'

    def purchase_info(self, obj):
        fertilizer_fields = [
            ('crop1','crop_stage1','fertilizer1', 'quantity1', 'purchase_date1'),
            ('crop2','crop_stage2','fertilizer2', 'quantity2', 'purchase_date2'),
            ('crop3','crop_stage3','fertilizer3', 'quantity3', 'purchase_date3'),
            ('crop4','crop_stage4','fertilizer4', 'quantity4', 'purchase_date4'),
            ('crop5','crop_stage5','fertilizer5', 'quantity5', 'purchase_date5'),
        ]
        fertilizer_data = {}
        for crop, crop_stage, fertilizer, quantity, purchase_date in fertilizer_fields:
            crop = getattr(obj, crop)
            crop_stage = getattr(obj, crop_stage)
            fertilizer_name = getattr(obj, fertilizer)
            quantity_value = getattr(obj, quantity)
            purchase_date_value = getattr(obj, purchase_date)

            if crop and crop_stage and fertilizer_name and quantity_value and purchase_date_value:
                formatted_date = purchase_date_value.strftime('%d-%m-%Y')
                if formatted_date in fertilizer_data:
                    fertilizer_data[formatted_date].append((crop, crop_stage,fertilizer_name, quantity_value))
                else:
                    fertilizer_data[formatted_date] = [(crop, crop_stage, fertilizer_name, quantity_value)]
        table = '<table>'
        for date, products in fertilizer_data.items():
            table += f"<tr><td rowspan='{len(products)}'><strong>{date}</strong></td>"
            for index, (crop, crop_stage, fertilizer_name, quantity_value) in enumerate(products):
                if index > 0:
                    table += "<tr>"
                table += (
                    f"<td>{crop}</td><td>{crop_stage}</td><td>{fertilizer_name}</td><td>{quantity_value}</td></tr>"
                )
        table += '</table>'
        return mark_safe(table) if table != '<table></table>' else '-'

    purchase_info.short_description = 'Purchase-Info'   

@admin.register(Crop)
class CropAdmin(admin.ModelAdmin):
    list_display = ['name','blanket_n_value','blanket_p_value','blanket_k_value','stage_one_n_value','stage_one_p_value','stage_one_k_value','stage_two_n_value','stage_two_p_value','stage_two_k_value','stage_three_n_value','stage_three_p_value','stage_three_k_value']


@admin.register(Advisor)
class AdvisorAdmin(admin.ModelAdmin):
    list_display = ['name','whatsapp_no','crop','crop_area', 'available_of_str', 'ph_value',
                    'n_value', 'p_value', 'k_value','nitrogen', 'phosphorus', 'potassium','crop_stage']

class ExistingUserProfileAdmin(admin.ModelAdmin):
    list_display = ['customer_name','username','password']

    def customer_name(self, obj):
        return obj.customer.name if obj.customer else ""
    
class AgMachineSpecificationsAdmin(admin.ModelAdmin):
    list_display = ['product_name', 'crop', 'land_extent', 'price', 'soil_condition', 'unit']

class AgMachineXUserInputAdmin(admin.ModelAdmin):
    list_display = ['machinery_req', 'full_name', 'whatsapp_no']

class FBIEnquiryAdmin(admin.ModelAdmin):
    list_display = ['user_name', 'phone_no', 'get_crop']

    def get_crop(self, obj):
        return obj.crop
    get_crop.short_description = 'Selected Crops'

class NutriTrackerScheduleAdmin(admin.ModelAdmin):
    list_display = ['crops','crop_types', 'crop_stage', 'scheduling_period']

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

class ATSContactProductImagesInline(admin.StackedInline):
      model = ATSContactProductImages
      extra = 1

class ATSContactProductInfoInline(admin.StackedInline):
      model = ATSContactProductInfo
      extra = 1
      
class ATSContactInfoAdmin(admin.ModelAdmin):
      inlines = [ATSContactProductInfoInline, ATSContactProductImagesInline]
      list_display = ['category','contact_company_name','contact_name','contact_email']

class ATSSellerProductImageInline(admin.StackedInline):
      model=ATSSellerProductImage
      extra=0
      
class ATSSellerAdmin(admin.ModelAdmin):
	inlines=[ATSSellerProductImageInline]
	list_display = ['seller_name','seller_company','seller_email_id']


class ATSInfoAdmin(admin.ModelAdmin):
      list_display = ['category_name']
      prepopulated_fields={'category_slug':('category_name', )}

admin.site.register(MarketPlannerStrategy)
admin.site.register(FundRequirement)
admin.site.register(Feedback, FeedbackAdmin)
admin.site.register(AddedServices, AddedServiceAdmin)
admin.site.register(UserProfile, UserProfileAdmin) 
admin.site.register(NewFarmerPurchaseHistory,NewFarmerPurchaseHistoryAdmin)
admin.site.register(NutriTracker, NutriTrackerAdmin)
admin.site.register(ExistingUserProfile, ExistingUserProfileAdmin)
admin.site.register(AgMachineSpecifications, AgMachineSpecificationsAdmin)
admin.site.register(AgMachineXUserInput,AgMachineXUserInputAdmin)
admin.site.register(AgriFBI, AgriFBIAdmin)
admin.site.register(FBIEnquiry, FBIEnquiryAdmin)
admin.site.register(CropIntelKnowledge, CropIntelKnowlegeAdmin)
admin.site.register(CropIntelInput)
admin.site.register(NutriTrackerSchedule, NutriTrackerScheduleAdmin)
admin.site.register(DiseaseRecognition)
admin.site.register(ACProductNPK, ACProductNPKAdmin)
admin.site.register(SymptomRecognitionKnowledge)
admin.site.register(SymptomsRecognitionInput)
admin.site.register(Highlights)
admin.site.register(ATSIntro)
admin.site.register(ATSInfo, ATSInfoAdmin)
admin.site.register(ATSContactInfo, ATSContactInfoAdmin)
admin.site.register(ATSSeller, ATSSellerAdmin)
admin.site.register(ATSRoadmap)
admin.site.register(Contact,ContactAdmin)
admin.site.register(SeoContent)
admin.site.register(Brands)
admin.site.register(Credentials)
admin.site.register(NotificationRecord)
admin.site.register(IntroTextDescription,IntroTextDescriptionAdmin)
admin.site.register(ContactNumber,ContactNumberAdmin)