from django.db import models
from django.contrib.auth.hashers import make_password
from django.contrib.auth.models import User
from cloudinary.models import CloudinaryField
from django.core.exceptions import ValidationError
from django.core.validators import MaxValueValidator, MinValueValidator
import calendar
import datetime
from multiselectfield import MultiSelectField
import itertools

class IntroTextDescription(models.Model):
     Englishdescription=models.TextField(null=False)
     Kannadadescription=models.TextField(null=True)
     class Meta:
         verbose_name = 'Enter Kannada and English Description AGI'
         verbose_name_plural = 'Enter Kannada and English Description AGI'

#SEO Content for Web Pages
class SeoContent(models.Model):
	PAGES = (('home','Home'),
             ('aboutus','About Us'),
             ('contactus','Contact Us'),
             ('cropintel','CropIntel'),
             ('agmachinex','AgMachineX'),
             ('agriclinic','AgriClinic'),
             ('fbi','FBI'),
             ('nutitracker','NutriTracker'),)
	page = models.CharField(max_length=50, choices=PAGES)
	meta_title = models.CharField(max_length=255, null=True, blank=True)
	meta_description = models.TextField(null=True, blank=True)
	backlinks = models.TextField(null=True, blank=True)
	keywords = models.TextField(null=True, blank=True)

	def __str__(self):
		return self.page

	class Meta:
		verbose_name = 'Enter SEO Content for WebPages'
		verbose_name_plural = 'Enter SEO Content for WebPages'

#Home Page: Cross Promotion Content 
class Highlights(models.Model):
	image = CloudinaryField()
	alt = models.CharField(max_length = 500, default='')
	link = models.CharField(max_length=255, blank=True, null=True)
	text1 = models.CharField(max_length=255, blank=True, null=True)

	def __str__(self):
		return self.alt  

	class Meta:
		verbose_name = 'Enter Cross Promotion Content '
		verbose_name_plural = 'Enter Cross Promotion Content'

# Contact in Footer
class ContactNumber(models.Model):
    phone_number = models.CharField(max_length=20)
    Time = models.DateTimeField(auto_now_add=True)
    city = models.CharField(max_length=100, null=True, blank=True)
    remarks = models.CharField(max_length=500, null=True, blank=True)
    region = models.CharField(max_length=20, null=True)

    def __str__(self):
        return f"{self.phone_number} - {self.Time}"

    class Meta:
        verbose_name = 'Contact Number'
        verbose_name_plural = 'Contact Number'
		
#About Us Page: Collabration Section Images 
class Brands(models.Model):
	image = CloudinaryField(null=True)
	alt = models.CharField(max_length=255)

	def __str__(self):
		return self.alt

	class Meta:
		verbose_name = 'Upload Collabration Images'
		verbose_name_plural = 'Upload Collabration Images'

#About Us Page: For Credential Section 
class Credentials(models.Model):
	CATEGORY = (('awards','Awards'),
                ('media coverages','Media Coverages'),
                ('approvals and licenses','Approvals and Licenses'))
	image = CloudinaryField(null=True)
	title = models.CharField(max_length=255,null=True)
	type_of_image = models.CharField(max_length=255,choices=CATEGORY,null=True)

	class Meta:
		verbose_name = 'Upload Credential Images'
		verbose_name_plural = 'Upload Credential Images'

#Contact Us: Form
class Contact(models.Model):
	name = models.CharField(max_length=255)
	phone = models.CharField(max_length=10,null=True)
	place=models.CharField(max_length=500,default='')
	comments = models.TextField(null=True)
	date = models.DateTimeField(auto_now=True)
	is_seen=models.BooleanField(null=True)

	def __str__(self):
		return self.name

	class Meta:
		verbose_name = 'Get User Messages from Contact Us'
		verbose_name_plural = 'Get User Messages from Contact Us'

#Registered New User Model : from Register, Login and Compelete Profile
class UserProfile(models.Model):
	ZONE_DISTRICT = (('Anantapur', 'Anantapur'),
                     ('Bagalkot', 'Bagalkot'),
                     ('Bengaluru Rural', 'Bengaluru Rural'),
                     ('Belgaum', 'Belgaum'),
                     ('Bidar', 'Bidar'),
                     ('Bijapur(Vijayapura)', 'Bijapur(Vijayapura)'),
                     ('Bellary', 'Bellary'),
                     ('Chamarajanagar','Chamarajanagar'),
                     ('Chikkaballapur','Chikkaballapur'),
                     ('Chikmagalur(East)', 'Chikmagalur(East)'),
                     ('Chikmagalur(West)', 'Chikmagalur(West)'),
                     ('Chittoor(Andhra Pradesh)', 'Chittoor(Andhra Pradesh)'),
                     ('Chitradurga', 'Chitradurga'),
                     ('Coorg(Madikeri)(Kodagu))','Coorg(Madikeri)(Kodagu))'),
                     ('Dakshina Kannada(Mangalore)', 'Dakshina Kannada(Mangalore)'),
                     ('Davanagere', 'Davanagere'),
                     ('Dharwad', 'Dharwad'),
                     ('Gadag', 'Gadag'),
                     ('Gulbarga(Kalaburgi)', 'Gulbarga(Kalaburgi)'),
                     ('Haveri', 'Haveri'),
                     ('Hassan', 'Hassan'),
                     ('Kasargod(Kerala)', 'Kasargod(Kerala)'),
                     ('Kolar', 'Kolar'),
                     ('Koppala', 'Koppala'),
                     ('Krishangiri(Tamil Nadu)', 'Krishangiri(Tamil Nadu)'),
                     ('Mysuru', 'Mysuru'),
                     ('Mandya', 'Mandya'),
                     ('Nilgiris(Tamil Nadu)', 'Nilgiris(Tamil Nadu)'),
                     ('Raichur', 'Raichur'),
                     ('Ramanagara', 'Ramanagara'),
                     ('Shimoga', 'Shimoga'),
                     ('Tumkur', 'Tumkur'),
                     ('Udupi', 'Udupi'),
                     ('Uttara Kannada(East)', 'Uttara Kannada(East)'),
                     ('Uttara Kannada(West)', 'Uttara Kannada(West)'),
                     ('Wayanad(Kerala)', 'Wayanad(Kerala)'),
                     ('Yadgir', 'Yadgir'))

	TALUKS = (('Afzalpur', 'Afzalpur'),
			 ('Alur', 'Alur'),
			 ('Ankola', 'Ankola'),
			 ('Arkalgud', 'Arkalgud'),
			 ('Arsikere', 'Arsikere'),
			 ('Athani', 'Athani'),
			 ('Aurad', 'Aurad'),
			 ('Badami', 'Badami'),
			 ('Bagalkot', 'Bagalkot'),
			 ('Bagepalli', 'Bagepalli'),
			 ('Bailhongal', 'Bailhongal'),
			 ('Bangarapet', 'Bangarapet'),
			 ('Bantwal', 'Bantwal'),
			 ('Basavana Bagevadi', 'Basavana Bagevadi'),
			 ('Basavakalyan', 'Basavakalyan'),
			 ('Belthangady', 'Belthangady'),
			 ('Belur', 'Belur'),
			 ('Bhadravathi', 'Bhadravathi'),
			 ('Bhalki', 'Bhalki'),
			 ('Bijapur', 'Bijapur'),
			 ('Bilagi', 'Bilagi'),
			 ('Bhatkal', 'Bhatkal'),
			 ('Byadagi', 'Byadagi'),
		 	 ('Challakere', 'Challakere'),
 			 ('Chamarajanagar', 'Chamarajanagar'),
 			 ('Channagiri', 'Channagiri'),
 			 ('Channapatna', 'Channapatna'),
 			 ('Channarayapatna', 'Channarayapatna'),
 			 ('Chiknayakanhalli', 'Chiknayakanhalli'),
 			 ('Chikodi', 'Chikodi'),
 			 ('Chincholi', 'Chincholi'),
 			 ('Chintamani', 'Chintamani'),
 			 ('Chitapur', 'Chitapur'),
 			 ('Devanahalli', 'Devanahalli'),
		 	 ('Devadurga', 'Devadurga'),
 			 ('Doddaballapura', 'Doddaballapura'),
 			 ('Gangawati', 'Gangawati'),
			 ('Gauribidanur', 'Gauribidanur'),
			 ('Gokak', 'Gokak'),
			 ('Gubbi', 'Gubbi'),
			 ('Gundlupet', 'Gundlupet'),
			 ('Haliyal', 'Haliyal'),
			 ('Hangal', 'Hangal'),
			 ('Harpanahalli', 'Harpanahalli'),
			 ('Hassan', 'Hassan'),
			 ('Heggadadevana Kote', 'Heggadadevana Kote'),
			 ('Hirekerur', 'Hirekerur'),
			 ('Hiriyur', 'Hiriyur'),
			 ('Holalkere', 'Holalkere'),
			 ('Holenarasipura', 'Holenarasipura'),
			 ('Homnabad', 'Homnabad'),
			 ('Hosadurga', 'Hosadurga'),
			 ('Hosakote', 'Hosakote'),
			 ('Hosapete (Hospet)', 'Hosapete (Hospet)'),
			 ('Hosanagara', 'Hosanagara'),
			 ('Hungund', 'Hungund'),
			 ('Hunsur', 'Hunsur'),
			 ('Hubballi (Hubli)', 'Hubballi (Hubli)'),
			 ('Indi', 'Indi'),
			 ('Jamkhandi', 'Jamkhandi'),	
			 ('Jagalur', 'Jagalur'),
			 ('Jevargi', 'Jevargi'),
			 ('Kalghatgi', 'Kalghatgi'),
			 ('Kampli', 'Kampli'),
			 ('Kanakapura', 'Kanakapura'),
			 ('Kanakagiri', 'Kanakagiri'),
			 ('Karkala', 'Karkala'),
			 ('Karwar', 'Karwar'),
			 ('Kadur', 'Kadur'),
			 ('Khanapur', 'Khanapur'),	
			 ('Koppa', 'Koppa'),
			 ('Krishnarajanagara', 'Krishnarajanagara'),
			 ('Kudligi', 'Kudligi'),
			 ('Kundapura', 'Kundapura'),
			 ('Kundgol', 'Kundgol'),
			 ('Kunigal', 'Kunigal'),
	 	 	 ('Kushtagi', 'Kushtagi'),
			 ('Lingsugur', 'Lingsugur'),
			 ('Madikeri', 'Madikeri'),
			 ('Madhugiri', 'Madhugiri'),
             ('Maddur', 'Maddur'),
			 ('Madikeri', 'Madikeri'),
			 ('Magadi', 'Magadi'),
			 ('Malavalli', 'Malavalli'),
			 ('Malur', 'Malur'),
			 ('Manvi', 'Manvi'),
			 ('Maski', 'Maski'),
			 ('Mangalore', 'Mangalore'),
			 ('Mulbagal', 'Mulbagal'),
			 ('Muddebihal', 'Muddebihal'),
			 ('Mudhol', 'Mudhol'),
			 ('Mudigere', 'Mudigere'),
			 ('Mundargi', 'Mundargi'),
			 ('Mundgod', 'Mundgod'),
			 ('Nanjangud', 'Nanjangud'),
			 ('Narasimharajapura', 'Narasimharajapura'),
			 ('Nelamangala', 'Nelamangala'),
			 ('Pandavapura', 'Pandavapura'),
			 ('Pavagada', 'Pavagada'),
			 ('Piriyapatna', 'Piriyapatna'),
			 ('Puttur', 'Puttur'),
			 ('Raichur', 'Raichur'),
			 ('Ramdurg', 'Ramdurg'),
			 ('Ranibennur', 'Ranibennur'),
			 ('Raybag', 'Raybag'),
			 ('Sakleshpur', 'Sakleshpur'),
			 ('Sandur', 'Sandur'),
			 ('Saundatti-Yellamma', 'Saundatti-Yellamma'),
			 ('Sedam', 'Sedam'),
			 ('Shahapur', 'Shahapur'),
			 ('Shikaripura', 'Shikaripura'),
	 		 ('Shirahatti', 'Shirahatti'),
			 ('Shivamogga (Shimoga)', 'Shivamogga (Shimoga)'),
			 ('Shorapur', 'Shorapur'),
			 ('Sidlaghatta', 'Sidlaghatta'),
			 ('Sindhanur', 'Sindhanur'),
			 ('Sindgi', 'Sindgi'),
			 ('Sirsi', 'Sirsi'),
			 ('Siruguppa', 'Siruguppa'),
			 ('Sira', 'Sira'),
			 ('Srirangapatna', 'Srirangapatna'),
			 ('Somwarpet', 'Somwarpet'),
			 ('Sorab', 'Sorab'),
			 ('Sringeri', 'Sringeri'),
			 ('Srinivaspur', 'Srinivaspur'),
			 ('Sullia', 'Sullia'),
			 ('Talikota', 'Talikota'),
			 ('Tarikere', 'Tarikere'),
			 ('Thirthahalli', 'Thirthahalli'),
			 ('Tiptur', 'Tiptur'),
			 ('Tumkur', 'Tumkur'),
			 ('Udupi', 'Udupi'),
			 ('Virajpet', 'Virajpet'),
			 ('Yadgir', 'Yadgir'),
			 ('Yelbarga', 'Yelbarga'),
			 ('Yellapur', 'Yellapur'))

	# new user profile infor after registeration
	user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='profile')
	name = models.CharField(max_length=500)
	whatsapp_no = models.CharField(max_length=10)
	email = models.CharField(max_length=500, null=True, blank=True)
	# new and existing user profile info after login from 3rd Party API
	state = models.CharField(max_length=255, null=True, blank=True)
	district = models.CharField(max_length=500, blank=True, null=True)
	zone_district=models.CharField(max_length=500,choices=ZONE_DISTRICT,blank=True,null=True)
	#new and existing user profile info after "Complete Profile" section
	taluk = models.CharField(max_length=500, choices=TALUKS, null=True, blank=True)
	village = models.CharField(max_length=500, default='')
	zip_code = models.CharField(max_length=6, default='')
	zone = models.CharField(max_length=500, null=True, blank=True)

	def __str__(self):
		return self.user.username

	class Meta:
		verbose_name = 'Get Registered User Profile Info'
		verbose_name_plural = 'Get Registered User Profile Info'

#Registered New and Existing User Profile Plot Info
class Plot(models.Model):
	SOIL_CONDITION = (('Soft','Soft'),
                      ('Hard','Hard'),
                      ('With Stone','With Stone'))
	SOIL_HEALTH = (('Good','Good'),
                   ('Average','Average'),
                   ('Poor','Poor'))
	pH = (('Less than 6.5 (Acidic)','Less than 6.5(Acidic)'),
          ('6.5 - 7.5 (Neutral)','6.5 - 7.5 (Neutral)'),
          ('Higher than 7.5 (Alkaline)','Higher than 7.5 (Alkaline)'),)
	SOIL_NUTRIENTS = (('Organic Matter','Organic Matter'),
                      ('Nitrogen (N)','Nitrogen (N)'),
                      ('Phosphorus (P)','Phosphorus (P)'),
                      ('Potassium (K)','Potassium (K)'),
                      ('Calcium (Ca)','Calcium (Ca)'),
                      ('Magnesium (Mg)','Magnesium (Mg)'),
                      ('Sulphur(S)','Sulphur(S)'),
                      ('Iron (Fe)','Iron (Fe)'),
                      ('Manganese (Mn)','Manganese (Mn)'),
                      ('Zinc (Zn)','Zinc (Zn)'),
                      ('Copper (Cu)','Copper (Cu)'),
                      ('Boron (B)','Boron (B)'),
                      ('Molybdenum (Mo)','Molybdenum (Mo)'))
	WATER_SOURCES = (('Rain Fed','Rain Fed'),
                     ('Borewell','Borewell'),
                     ('Others','Others'))
	WATER_SUFFICIENCIES = (('Very Good Water Availability','Very Good Water Availability'),
                           ('Good Water Availability','Good Water Availability'),
                           ('Average Water Availability','Average Water Availability'),
                           ('Limited Water Availability','Limited Water Availability'),
                           ('Poor Water Availability','Poor Water Availability'))
	CROPS = (('Amla','Amla'),
             ('Areca New','Areca New'),
             ('Avocado','Avocado'),
             ('Arecanut','Arecanut'),
             ('Banana', 'Banana'),
             ('Betelvine','Betelvine'),
             ('Carrot','Carrot'),
             ('Cashewnut','Cashewnut'),
             ('Cauliflower (Cole Crops)','Cauliflower (Cole Crops)'),
             ('Chilli','Chilli'),
             ('Chrysanthemum','Chrysanthemum'),
             ('Citrus','Citrus'),
             ('Cocoa','Cocoa'),
             ('Coconut', 'Coconut'),
             ('Coffee','Coffee'),
             ('Cotton', 'Cotton'),
             ('Curry Leaves','Curry Leaves'),
             ('Custard Apple','Custard Apple'),
             ('Dragon Fruit','Dragon Fruit'),
             ('Drumstick','Drumstick'),
             ('Durian','Durian'),
             ('Fig','Fig'),
             ('Ginger','Ginger'),
             ('Grapes','Grapes'),
             ('Groundnut','Groundnut'),
             ('Guava','Guava'),
             ('Jack Fruit','Jack Fruit'),
             ('Jasmin','Jasmin'),
             ('Kokum','Kokum'),
             ('Lime','Lime'),
             ('Macadamia','Macadamia'),
             ('Mahogani','Mahogani'),
             ('Maize','Maize'),
             ('Mango','Mango'),
             ('Mangosteen','Mangosteen'),
             ('Mosambi','Mosambi'),
             ('Nutmeg','Nutmeg'),
             ('Onion','Onion'),
             ('Paddy','Paddy'),
             ('Papaya','Papaya'),
             ('Pepper','Pepper'),
             ('Pineapple','Pine apple'),
             ('Pomegranate','Pomegranate'),
             ('Potato','Potato'),
             ('Rambutan','Rambutan'),
             ('Rose','Rose'),
             ('Rosewood','Rosewood'),
             ('Sapota','Sapota'),
             ('Sugarcane','Sugarcane'),
             ('Tender Coconut','Tender Coconut'),
             ('Tomato','Tomato'),
             ('Tur','Tur'),
             ('Turmeric','Turmeric'),)
	user_profile = models.ForeignKey(UserProfile, on_delete=models.CASCADE)
	plot_name = models.CharField(max_length=500, blank=True, null=True)
	crop_grown = models.CharField(max_length=500, choices=CROPS, blank=True, null=True)
	land_area = models.CharField(max_length=100, blank=True, null=True)
	soil_condition = models.CharField(max_length=255, choices=SOIL_CONDITION, blank=True, null=True)
	soil_health = models.CharField(max_length=255, choices=SOIL_HEALTH, blank=True, null=True)
	soil_ph = models.CharField(max_length=255, choices=pH, blank=True, null=True)
	soil_rich_nutrients = models.CharField(max_length=255, choices=SOIL_NUTRIENTS, blank=True, null=True)
	soil_average_nutrients = models.CharField(max_length=255, choices=SOIL_NUTRIENTS, blank=True, null=True)
	soil_poor_nutrients = models.CharField(max_length=255, choices=SOIL_NUTRIENTS, blank=True, null=True)
	water_source = models.CharField(max_length=255, choices=WATER_SOURCES, blank=True, null=True)
	water_availability = models.CharField(max_length=255, choices=WATER_SUFFICIENCIES, blank=True, null=True)

	class Meta:
		verbose_name = 'Get Registered User Plot Info'
		verbose_name_plural = 'Get Registered User Plot Info'
		

#Nutritracker Stored Data: Existing User NutriTracker Specific Info
# class NutriTracker(models.Model):
# 	STATES = (('Andhra Pradesh', 'Andhra Pradesh'),
#               ('Andaman and Nicobar Islands','Andaman and Nicobar Islands'),
#               ('Arunachal Pradesh', 'Arunachal Pradesh'),
#               ('Assam','Assam'),
#               ('Bihar','Bihar'),
#               ('Chhattisgarh','Chhattisgarh'),
#               ('Chandigarh','Chandigarh'),
#               ('Dadra and Nagar Haveli and Daman and Diu','Dadra and Nagar Haveli and Daman and Diu'),
#               ('Delhi','Delhi'),
#               ('Goa','Goa'),
#               ('Gujarat','Gujarat'),
#               ('Haryana','Haryana'),
#               ('Himachal Pradesh','Himachal Pradesh'),
#               ('Jammu and Kashmir','Jammu and Kashmir'),
#               ('Jharkhand','Jharkhand'),
#               ('Karnataka','Karnataka'),
#               ('Kerala','Kerala'),
#               ('Lakshadweep','Lakshadweep'),
#               ('Madhya Pradesh','Madhya Pradesh'),
#               ('Maharashtra','Maharashtra'),
#               ('Manipur','Manipur'),
#               ('Meghalaya','Meghalaya'),
#               ('Mizoram','Mizoram'),
#               ('Nagaland','Nagaland'),
#               ('Odisha','Odisha'),
#               ('Punjab','Punjab'),
#               ('Puducherry','Puducherry'),
#               ('Rajasthan','Rajasthan'),
#               ('Sikkim','Sikkim'),
#               ('Tamil Nadu','Tamil Nadu'),
#               ('Telangana','Telangana'),
#               ('Tripura','Tripura'),
#               ('Uttar Pradesh','Uttar Pradesh'),
#               ('Uttarakhand','Uttarakhand'),
#               ('West Bengal','West Bengal'))
# 	DISTRICTS = (('Bagalkot','Bagalkot'),
#                  ('Ballari (Bellary)','Ballari (Bellary)'),
#                  ('Belagavi (Belgaum)','Belagavi (Belgaum)'),
#                  ('Bengaluru Rural','Bengaluru Rural'),
#                  ('Bengaluru Urban','Bengaluru Urban'),
#                  ('Bidar','Bidar'),
#                  ('Chamarajanagar','Chamarajanagar'),
#                  ('Chikballapur','Chikballapur'),
#                  ('Chikkamagaluru (Chikmagalur)','Chikkamagaluru (Chikmagalur)'),
#                  ('Chitradurga','Chitradurga'),
#                  ('Dakshina Kannada','Dakshina Kannada'),
#                  ('Davanagere','Davanagere'),
#                  ('Dharwad','Dharwad'),
#                  ('Gadag','Gadag'),
#                  ('Hassan','Hassan'),
#                  ('Haveri','Haveri'),
#                  ('Kalaburagi (Gulbarga)','Kalaburagi (Gulbarga)'),
#                  ('Kodagu (Coorg)','Kodagu (Coorg)'),
#                  ('Kolar','Kolar'),
#                  ('Koppal','Koppal'),
#                  ('Mandya','Mandya'),
#                  ('Mysuru (Mysore)','Mysuru (Mysore)'),
#                  ('Raichur','Raichur'),
#                  ('Ramanagara','Ramanagara'),
#                  ('Shivamogga (Shimoga)','Shivamogga (Shimoga)'),
#                  ('Tumakuru (Tumkur)','Tumakuru (Tumkur)'),
#                  ('Udupi','Udupi'),
#                  ('Uttara Kannada (Karwar)','Uttara Kannada (Karwar)'),
#                  ('Vijayapura (Bijapur)','Vijayapura (Bijapur)'),
#                  ('Yadgir','Yadgir'))
# 	TALUKS = (('Afzalpur', 'Afzalpur'),
# 			 ('Alur', 'Alur'),
# 			 ('Ankola', 'Ankola'),
# 			 ('Arkalgud', 'Arkalgud'),
# 			 ('Arsikere', 'Arsikere'),
# 			 ('Athani', 'Athani'),
# 			 ('Aurad', 'Aurad'),
# 			 ('Badami', 'Badami'),
# 			 ('Bagalkot', 'Bagalkot'),
# 			 ('Bagepalli', 'Bagepalli'),
# 			 ('Bailhongal', 'Bailhongal'),
# 			 ('Bangarapet', 'Bangarapet'),
# 			 ('Bantwal', 'Bantwal'),
# 			 ('Basavana Bagevadi', 'Basavana Bagevadi'),
# 			 ('Basavakalyan', 'Basavakalyan'),
# 			 ('Belthangady', 'Belthangady'),
# 			 ('Belur', 'Belur'),
# 			 ('Bhadravathi', 'Bhadravathi'),
# 			 ('Bhalki', 'Bhalki'),
# 			 ('Bijapur', 'Bijapur'),
# 			 ('Bilagi', 'Bilagi'),
# 			 ('Bhatkal', 'Bhatkal'),
# 			 ('Byadagi', 'Byadagi'),
# 		 	 ('Challakere', 'Challakere'),
#  			 ('Chamarajanagar', 'Chamarajanagar'),
#  			 ('Channagiri', 'Channagiri'),
#  			 ('Channapatna', 'Channapatna'),
#  			 ('Channarayapatna', 'Channarayapatna'),
#  			 ('Chiknayakanhalli', 'Chiknayakanhalli'),
#  			 ('Chikodi', 'Chikodi'),
#  			 ('Chincholi', 'Chincholi'),
#  			 ('Chintamani', 'Chintamani'),
#  			 ('Chitapur', 'Chitapur'),
#  			 ('Devanahalli', 'Devanahalli'),
# 		 	 ('Devadurga', 'Devadurga'),
#  			 ('Doddaballapura', 'Doddaballapura'),
#  			 ('Gangawati', 'Gangawati'),
# 			 ('Gauribidanur', 'Gauribidanur'),
# 			 ('Gokak', 'Gokak'),
# 			 ('Gubbi', 'Gubbi'),
# 			 ('Gundlupet', 'Gundlupet'),
# 			 ('Haliyal', 'Haliyal'),
# 			 ('Hangal', 'Hangal'),
# 			 ('Harpanahalli', 'Harpanahalli'),
# 			 ('Hassan', 'Hassan'),
# 			 ('Heggadadevana Kote', 'Heggadadevana Kote'),
# 			 ('Hirekerur', 'Hirekerur'),
# 			 ('Hiriyur', 'Hiriyur'),
# 			 ('Holalkere', 'Holalkere'),
# 			 ('Holenarasipura', 'Holenarasipura'),
# 			 ('Homnabad', 'Homnabad'),
# 			 ('Hosadurga', 'Hosadurga'),
# 			 ('Hosakote', 'Hosakote'),
# 			 ('Hosapete (Hospet)', 'Hosapete (Hospet)'),
# 			 ('Hosanagara', 'Hosanagara'),
# 			 ('Hungund', 'Hungund'),
# 			 ('Hunsur', 'Hunsur'),
# 			 ('Hubballi (Hubli)', 'Hubballi (Hubli)'),
# 			 ('Indi', 'Indi'),
# 			 ('Jamkhandi', 'Jamkhandi'),	
# 			 ('Jagalur', 'Jagalur'),
# 			 ('Jevargi', 'Jevargi'),
# 			 ('Kalghatgi', 'Kalghatgi'),
# 			 ('Kampli', 'Kampli'),
# 			 ('Kanakapura', 'Kanakapura'),
# 			 ('Kanakagiri', 'Kanakagiri'),
# 			 ('Karkala', 'Karkala'),
# 			 ('Karwar', 'Karwar'),
# 			 ('Kadur', 'Kadur'),
# 			 ('Khanapur', 'Khanapur'),	
# 			 ('Koppa', 'Koppa'),
# 			 ('Krishnarajanagara', 'Krishnarajanagara'),
# 			 ('Kudligi', 'Kudligi'),
# 			 ('Kundapura', 'Kundapura'),
# 			 ('Kundgol', 'Kundgol'),
# 			 ('Kunigal', 'Kunigal'),
# 	 	 	 ('Kushtagi', 'Kushtagi'),
# 			 ('Lingsugur', 'Lingsugur'),
# 			 ('Madikeri', 'Madikeri'),
# 			 ('Madhugiri', 'Madhugiri'),
#              ('Maddur', 'Maddur'),
# 			 ('Madikeri', 'Madikeri'),
# 			 ('Magadi', 'Magadi'),
# 			 ('Malavalli', 'Malavalli'),
# 			 ('Malur', 'Malur'),
# 			 ('Manvi', 'Manvi'),
# 			 ('Maski', 'Maski'),
# 			 ('Mangalore', 'Mangalore'),
# 			 ('Mulbagal', 'Mulbagal'),
# 			 ('Muddebihal', 'Muddebihal'),
# 			 ('Mudhol', 'Mudhol'),
# 			 ('Mudigere', 'Mudigere'),
# 			 ('Mundargi', 'Mundargi'),
# 			 ('Mundgod', 'Mundgod'),
# 			 ('Nanjangud', 'Nanjangud'),
# 			 ('Narasimharajapura', 'Narasimharajapura'),
# 			 ('Nelamangala', 'Nelamangala'),
# 			 ('Pandavapura', 'Pandavapura'),
# 			 ('Pavagada', 'Pavagada'),
# 			 ('Piriyapatna', 'Piriyapatna'),
# 			 ('Puttur', 'Puttur'),
# 			 ('Raichur', 'Raichur'),
# 			 ('Ramdurg', 'Ramdurg'),
# 			 ('Ranibennur', 'Ranibennur'),
# 			 ('Raybag', 'Raybag'),
# 			 ('Sakleshpur', 'Sakleshpur'),
# 			 ('Sandur', 'Sandur'),
# 			 ('Saundatti-Yellamma', 'Saundatti-Yellamma'),
# 			 ('Sedam', 'Sedam'),
# 			 ('Shahapur', 'Shahapur'),
# 			 ('Shikaripura', 'Shikaripura'),
# 	 		 ('Shirahatti', 'Shirahatti'),
# 			 ('Shivamogga (Shimoga)', 'Shivamogga (Shimoga)'),
# 			 ('Shorapur', 'Shorapur'),
# 			 ('Sidlaghatta', 'Sidlaghatta'),
# 			 ('Sindhanur', 'Sindhanur'),
# 			 ('Sindgi', 'Sindgi'),
# 			 ('Sirsi', 'Sirsi'),
# 			 ('Siruguppa', 'Siruguppa'),
# 			 ('Sira', 'Sira'),
# 			 ('Srirangapatna', 'Srirangapatna'),
# 			 ('Somwarpet', 'Somwarpet'),
# 			 ('Sorab', 'Sorab'),
# 			 ('Sringeri', 'Sringeri'),
# 			 ('Srinivaspur', 'Srinivaspur'),
# 			 ('Sullia', 'Sullia'),
# 			 ('Talikota', 'Talikota'),
# 			 ('Tarikere', 'Tarikere'),
# 			 ('Thirthahalli', 'Thirthahalli'),
# 			 ('Tiptur', 'Tiptur'),
# 			 ('Tumkur', 'Tumkur'),
# 			 ('Udupi', 'Udupi'),
# 			 ('Virajpet', 'Virajpet'),
# 			 ('Yadgir', 'Yadgir'),
# 			 ('Yelbarga', 'Yelbarga'),
# 			 ('Yellapur', 'Yellapur'))

# 	MONTH = ((calendar.month_name[i],calendar.month_name[i]) for i in range(1,13))
# 	MONTH1 = ((calendar.month_name[i],calendar.month_name[i]) for i in range(1,13))
# 	IRRIGATION = (('Flood Irrigation','Flood Irrigation'),
#                   ('Sprinkler Irrigation','Sprinkler Irrigation'),
#                   ('Drip Irrigation','Drip Irrigation'),
#                   ('Other Irrigation Method','Other Irrigation Method'))
# 	#User Info
# 	name = models.CharField(max_length=500)
# 	whatsapp_no = models.CharField(max_length=10, unique=True, null=True)
# 	email = models.EmailField(unique=True, null=True, blank=True)
# 	state = models.CharField(max_length=255, choices=STATES)
# 	district = models.CharField(max_length=500, blank=True, null=True, choices=DISTRICTS)
# 	taluk = models.CharField(max_length=500, choices=TALUKS, null=True, blank=True)
# 	village = models.CharField(max_length=500, default='')
# 	zip_code = models.CharField(max_length=6, default='')
# 	zone = models.CharField(max_length=500, null=True, blank=True)
# 	crop_density = models.CharField(max_length=255, blank=True, null=True)
# 	planting_month = models.CharField(max_length=255, blank=True, null=True, choices=MONTH)
# 	harvesting_month = models.CharField(max_length=255, blank=True, null=True, choices=MONTH1)
# 	nitrogen = models.CharField(max_length=255, blank=True, null=True)
# 	potassium = models.CharField(max_length=255, blank=True, null=False) 
# 	phosphorous = models.CharField(max_length=255, blank=True, null=True)
# 	secondary_nutrients = models.CharField(max_length=255, blank=True, null=True)
# 	micro_nutrients = models.CharField(max_length=255, blank=True, null=True)
# 	organic_carbon = models.CharField(max_length=500, null=True, blank=True)
# 	irrigation_method = models.CharField(max_length=500, null=True, blank=True, choices=IRRIGATION)
# 	other_irrigation = models.CharField(max_length=500, null=True, blank=True)
# 	nutrients_freq = models.IntegerField(null=True, blank=True,default=0)

# 	def __str__(self):
# 		return self.name

# 	class Meta:
# 		verbose_name = 'NutriTracker Existing User Fertilizer Purchase Info'
# 		verbose_name_plural = 'NutriTracker Existing User Fertilizer Purchase Info'

#NutriTracker Stored Data: Existing User Fertilizer Purchase Info. this model is inline with NutriTracker Model in admin.py
# class ProductPurchased(models.Model):
# 	CROPS = (('Potato','Potato'),
# 			 ('Tomato', 'Tomato'),
# 			 ('Banana', 'Banana'),
#     		 ('Sugarcane','Sugarcane'),
# 			 ('Coffee', 'Coffee'),
# 			 ('Pepper','Pepper'),
# 			 ('Pappya','Pappya'),)
# 	AGRICLINIC = (('Dr Soil Health', 'Dr Soil Health'),
# 				  ('Dr Soil Health Areca Special', 'Dr Soil Health Areca Special'),
# 				  ('Bio NPK', 'Bio NPK'),
# 				  ('Bio Potash', 'Bio Potash'),
#     			  ('Spirusan','Spirusan'),
# 				  ('Amruth Banana Microbial Consortia','Amruth Banana Microbial Consortia'),
# 				  ('Amruth Vegetable Microbial Consortia','Amruth Vegetable Microbial Consortia'),
# 				  ('Amruth Sugarcane Microbial Consortia','Amruth Sugarcane Microbial Consortia'),
# 				  ('Amruth Areca Microbial Consortia','Amruth Areca Microbial Consortia'),
# 				  ('Humigreen','Humigreen'),
# 				  ('Jeevarakshak','Jeevarakshak'),
# 				  ('Humisan','Humisan'),
# 				  ('Amino Gold','Amino Gold'),
# 				  ('Indozyme','Indozyme'),
# 				  ('Amruth Gold plus','Amruth Gold plus'),
# 				  ('Bio-k Rich','Bio-k Rich'),
# 				  ('Akshaya Areca Special','Akshaya Areca Special'),
# 				  ('Arka Waste Decomposer','Arka Waste Decomposer'),
# 				  ('Amezinc','Amezinc'),
# 				  ('AmStrong','AmStrong'),
# 				  ('Alzyme','Alzyme'),
# 				  ('Micro Speed','Micro Speed'),
# 				  ('Amruth Coffee Microbial Consortia','Amruth Coffee Microbial Consortia'),
# 				  ('Altraset','Altraset'),
# 				  ('Phos-Max','Phos-Max'),
# 				  ('Phyton T','Phyton T'),
# 				  ('MakeUp','MakeUp'),
# 				  ('ProGibb','ProGibb'),
# 				  ('Banana Micronutrient','Banana Micronutrient'),
# 				  ('Mango Micronutrient','Mango Micronutrient'),
# 				  ('Aquafert SOP','Aquafert SOP'),
#                   ('Gromor Spray 0-0-50','Gromor Spray 0-0-50'),
#                   ('GroMAG','GroMAG'),
#                   ('AcuMist Calcium','AcuMist Calcium'),
#                   ('Gromor Spray CN','Gromor Spray CN'),
#                   ('Gromor Sulphozinc','Gromor Sulphozinc'),
#                   ('Folibor','Folibor'),
#                   ('Tracel','Tracel'),
#                   ('Aquafert FPOV','Aquafert FPOV'),
#                   ('Gromor Spray 19:19:19','Gromor Spray 19:19:19'),
#                   ('Acuspray Sugarcane','Acuspray Sugarcane'),
#                   ('Power Plus','Power Plus'),
#                   ('Samrakshak','Samrakshak'),
#                   ('Alnym','Alnym'),
#                   ('Navarathna','Navarathna'),
#                   ('Alderm','Alderm'),
#                   ('Agri Nematode','Agri Nematode'),
#                   ('Almonas','Almonas'),
#                   ('Tatamida','Tatamida'),
#                   ('Sumipleo','Sumipleo'),
#                   ('Takumi','Takumi'),
#                   ('Reeva 5"%" EC','Reeva 5"%" EC'),
#                   ('Aaroosh','Aaroosh'),
#                   ('Blitox','Blitox'),
#                   ('Magnite','Magnite'))
# 	customer = models.ForeignKey(NutriTracker, on_delete=models.CASCADE, null=True)
# 	crop = models.CharField(max_length=500, null=True, blank=True, choices=CROPS)
# 	product_name = models.CharField(max_length=100, null=True, blank=True,choices=AGRICLINIC)
# 	quantity = models.CharField(max_length=10, null=True, blank=True)
# 	date = models.DateField(blank=True, null=True)

# 	class Meta:
# 		ordering = ['-date'] 
# 		verbose_name = 'NutriTracker Existing User Fertilizer Purchase Info'
# 		verbose_name_plural = 'NutriTracker Existing User Fertilizer Purchase Info'

# 	def __str__(self):
# 		return self.customer.name

#Credentials Creation for Existing Customer
class ExistingUserProfile(models.Model):
    # customer = models.ForeignKey(NutriTracker, on_delete=models.CASCADE, null=True, blank=True)
    username = models.CharField(max_length=200, null=True, blank=True)
    password = models.CharField(max_length=200, null=True, blank=True)

    class Meta:
        verbose_name = 'Get Existing User Credentials'
        verbose_name_plural = 'Get Existing User Credentials'

# NutriTracker User Input: New User/Farmer Fertilizer Purchase Info

# class NewFarmerPurchaseHistory(models.Model):
# 	IRRIGATION = (('Flood Irrigation','Flood Irrigation'),
#                   ('Sprinkler Irrigation','Sprinkler Irrigation'),
#                   ('Drip Irrigation','Drip Irrigation'),
#                   ('Other Irrigation Method','Other Irrigation Method'))
# 	MONTH = ((calendar.month_name[i],calendar.month_name[i]) for i in range(1,13))
# 	MONTH1 = ((calendar.month_name[i],calendar.month_name[i]) for i in range(1,13))
# 	#User Info
# 	name = models.CharField(max_length=255)
# 	whatsapp_no = models.CharField(max_length=255)
# 	email = models.CharField(max_length=255, null=True, blank=True)
# 	state = models.CharField(max_length=255, default='')
# 	district = models.CharField(max_length=500, blank=True, null=True, )
# 	taluk = models.CharField(max_length=500, null=True, blank=True)
# 	#Plot Info
# 	plot_name = models.CharField(max_length=500, blank=True, null=True)
# 	crop_grown = models.CharField(max_length=500, blank=True, null=True)
# 	land_area = models.CharField(max_length=100, blank=True, null=True)
# 	soil_condition = models.CharField(max_length=255, blank=True, null=True)
# 	soil_health = models.CharField(max_length=255, blank=True, null=True)
# 	soil_ph = models.CharField(max_length=255, blank=True, null=True) 
# 	soil_rich_nutrients = models.CharField(max_length=255, blank=True, null=True)
# 	soil_average_nutrients = models.CharField(max_length=255,blank=True, null=True)
# 	soil_poor_nutrients = models.CharField(max_length=255,  blank=True, null=True)
# 	water_source = models.CharField(max_length=255, blank=True, null=True)
# 	water_availability = models.CharField(max_length=255, blank=True, null=True)
# 	#NT Specific Info
# 	crop_density = models.CharField(max_length=255, blank=True, null=True)
# 	planting_month = models.CharField(max_length=255, blank=True, null=True, choices=MONTH)
# 	harvesting_month = models.CharField(max_length=255, blank=True, null=True, choices=MONTH1)
# 	nitrogen = models.CharField(max_length=255, blank=True, null=True)
# 	potassium = models.CharField(max_length=255, blank=True, null=False) 
# 	phosphorous = models.CharField(max_length=255, blank=True, null=True)
# 	secondary_nutrients = models.CharField(max_length=255, blank=True, null=True)
# 	micro_nutrients = models.CharField(max_length=255, blank=True, null=True)
# 	organic_carbon = models.CharField(max_length=500, null=True, blank=True)
# 	irrigation_method = models.CharField(max_length=500, null=True, blank=True, choices=IRRIGATION)
# 	other_irrigation = models.CharField(max_length=500, null=True, blank=True)
# 	nutrients_freq = models.IntegerField(null=True, blank=True,default=0)

# 	class Meta:
# 		verbose_name = 'NutriTracker New User Fertilizer Purchase Info'
# 		verbose_name_plural = 'NutriTracker New User Fertilizer Purchase Info'


#NutriTracker User Input: NutriTracker New User Fertilizer Purchase Info. This model is inline with NewFarmerPurchaseHistory model
# class NTFertilizerPurchase(models.Model):
#     CROPS = (('Amla','Amla'),
#              ('Areca New','Areca New'),
#              ('Avocado','Avocado'),
#              ('Arecanut','Arecanut'),
#              ('Banana', 'Banana'),
#              ('Betelvine','Betelvine'),
#              ('Carrot','Carrot'),
#              ('Cashewnut','Cashewnut'),
#              ('Cauliflower (Cole Crops)','Cauliflower (Cole Crops)'),
#              ('Chilli','Chilli'),
#              ('Chrysanthemum','Chrysanthemum'),
#              ('Citrus','Citrus'),
#              ('Cocoa','Cocoa'),
#              ('Coconut', 'Coconut'),
#              ('Coffee','Coffee'),
#              ('Cotton', 'Cotton'),
#              ('Curry Leaves','Curry Leaves'),
#              ('Custard Apple','Custard Apple'),
#              ('Dragon Fruit','Dragon Fruit'),
#              ('Drumstick','Drumstick'),
#              ('Durian','Durian'),
#              ('Fig','Fig'),
#              ('Ginger','Ginger'),
#              ('Grapes','Grapes'),
#              ('Groundnut','Groundnut'),
#              ('Guava','Guava'),
#              ('Jack Fruit','Jack Fruit'),
#              ('Jasmin','Jasmin'),
#              ('Kokum','Kokum'),
#              ('Lime','Lime'),
#              ('Macadamia','Macadamia'),
#              ('Mahogani','Mahogani'),
#              ('Maize','Maize'),
#              ('Mango','Mango'),
#              ('Mangosteen','Mangosteen'),
#              ('Mosambi','Mosambi'),
#              ('Nutmeg','Nutmeg'),
#              ('Onion','Onion'),
#              ('Paddy','Paddy'),
#              ('Papaya','Papaya'),
#              ('Pepper','Pepper'),
#              ('Pineapple','Pine apple'),
#              ('Pomegranate','Pomegranate'),
#              ('Potato','Potato'),
#              ('Rambutan','Rambutan'),
#              ('Rose','Rose'),
#              ('Rosewood','Rosewood'),
#              ('Sapota','Sapota'),
#              ('Sugarcane','Sugarcane'),
#              ('Tender Coconut','Tender Coconut'),
#              ('Tomato','Tomato'),
#              ('Tur','Tur'),
#              ('Turmeric','Turmeric'),)
#     STAGES = (('Early Stage','Early Stage'),
#         ('Vegetative Stage','Vegetative Stage'),
#         ('Yielding Stage','Yielding Stage'))
#     TYPE = (('Organic Fertilizer','Organic Fertilizer'),
#             ('Inorganic Fertilizer','Inorganic Fertilizer'),
#             ('FYM','FYM'))
#     Nutrients = (('Nitrogen','Nitrogen'),
#                  ('Potassium','Potassium'),
#                  ('Phosphorous','Phosphorous'),
#                  ('Calcium','Calcium'),
#                  ('Magenesium','Magenesium'),
#                  ('Manganese','Manganese'),
#                  ('Copper','Copper'),
#                  ('Zinc','Zinc'),
#                  ('Sulphur','Sulphur'),
#                  ('Boron','Boron'),
#                  ('Iron','Iron'),
#                  ('Molybdenum','Molybdenum'))
#     new_user_info = models.ForeignKey(NewFarmerPurchaseHistory, on_delete=models.CASCADE)
#     crop = models.CharField(max_length=100, choices=CROPS)
#     crop_stage = models.CharField(max_length=256, choices=STAGES)
#     fertilizer = models.CharField(max_length=500)
#     nutrients = models.CharField(max_length=500, choices=Nutrients)
#     fertilizer_type = models.CharField(max_length=500, choices=TYPE)
#     brand = models.CharField(max_length=500)
#     quantity = models.CharField(max_length=10)
#     purchase_date = models.DateField()
    
#     class Meta:
#         verbose_name = 'NutriTracker New User Fertilizer Purchase Info' 
#         verbose_name_plural = 'NutriTracker New User Fertilizer Purchase Info'
		

# #NutriTracker Stored Data: Crop-specific Schedule Info
# class NutriTrackerSchedule(models.Model):
#     CROPS = (('Potato','Potato'),
#              ('Tomato', 'Tomato'),
#              ('Banana', 'Banana'),
#              ('Sugarcane','Sugarcane'),
#              ('Coffee', 'Coffee'),
#              ('Pepper','Pepper'),
#              ('Pappya','Pappya'),)
#     STAGES = (('Early Stage', 'Early Stage'),
#               ('Yielding Stage','Yielding Stage'),
#               ('Flowering','Flowering'),
#               ('Growth Stage','Growth Stage'),
#               ('Fruiting','Fruiting'))
#     CROP_TYPES = (('Annual Crops','Annual Crops'),
#                   ('Perennial Crops','Perennial Crops'),
#                   ('Biannual Crops','Biannual Crops'),
#                   ('Biennial Crops','Biennial Crops'))
#     crops = models.CharField(max_length=500, choices=CROPS)
#     crop_stage = models.CharField(max_length=500, choices=STAGES)
#     crop_types = models.CharField(max_length=500, choices=CROP_TYPES)
#     scheduling_period = models.CharField(max_length=500)

#     class Meta:
#         verbose_name = 'NutriTracker Crop-Specific Scheduling Period Record'
#         verbose_name_plural = 'NutriTracker Crop-Specific Scheduling Period Record'

# #NutriTracker Notification Record Data 
# class NotificationRecord(models.Model):
# 	name = models.CharField(max_length=500)
# 	phone_no = models.CharField(max_length=10)
# 	email = models.EmailField(null=True, blank=True)
# 	notification_date = models.DateField()
# 	fertilizers = models.CharField(max_length=500)
# 	crop = models.CharField(max_length=500)
# 	message = models.TextField()

# 	class Meta:
# 		verbose_name = 'NutriTracker User-Notification Record'
# 		verbose_name_plural = 'NutriTracker User-Notification Record'


#AgMachineX Stored Data: Machineries Specifications   
class AgMachineSpecifications(models.Model):
	category = (('brush cutter', 'Brush Cutter'),
                ('power weeder', 'Power Weeder'),
                ('power tiller', 'Power Tiller'),
                ('water pump', 'Water Pump'),
                ('sprayer','Sprayer'),
                ('htp sprayer','HTP Sprayer'),
                ('earth auger','Earth Auger'),
                ('chainsaw','Chainsaw'),
                ('hedge trimmer','Hedge Trimmer'),
                ('chaff cutter','Chaff Cutter'),
                ('milking machine', 'Milking Machine'),
                ('lawn mower','Lawn Mower'),
                ('generator','Generator'),
                ('engine','Engine'),
                ('sprayer manual', 'Sprayer Manual'),
                ('milking machine manual', 'Milking Machine Manual'),
                ('coconut climber', 'Coconut Climber'))
	SOIL = (('Soft','Soft'),
            ('Hard','Hard'),
            ('With Stone','With Stone'))
	FMTYPE = (('Fuel','Fuel'),
              ('Battery','Battery'))
	PRODQUAL = (('Economical','Economical'),
                ('Premium','Premium'))
	IRRISOL = (('Permanent','Permanent'),
               ('Temporary','Temporary'))
	IRRITYPE = (('Drip','Drip'),
                ('Flood','Flood'),
                ('Sprinkler','Sprinkler'))
	IRRIUSAGE = (('Irrigation Only','Irrigation Only'),
                 ('Fertigation Included','Fertion Included'))
	CROPS = (('Amla','Amla'),
             ('Areca New','Areca New'),
             ('Avocado','Avocado'),
             ('Arecanut','Arecanut'),
             ('Banana', 'Banana'),
             ('Betelvine','Betelvine'),
             ('Carrot','Carrot'),
             ('Cashewnut','Cashewnut'),
             ('Cauliflower (Cole Crops)','Cauliflower (Cole Crops)'),
             ('Chilli','Chilli'),
             ('Chrysanthemum','Chrysanthemum'),
             ('Citrus','Citrus'),
             ('Cocoa','Cocoa'),
             ('Coconut', 'Coconut'),
             ('Coffee','Coffee'),
             ('Cotton', 'Cotton'),
             ('Curry Leaves','Curry Leaves'),
             ('Custard Apple','Custard Apple'),
             ('Dragon Fruit','Dragon Fruit'),
             ('Drumstick','Drumstick'),
             ('Durian','Durian'),
             ('Fig','Fig'),
             ('Ginger','Ginger'),
             ('Grapes','Grapes'),
             ('Groundnut','Groundnut'),
             ('Guava','Guava'),
             ('Jack Fruit','Jack Fruit'),
             ('Jasmin','Jasmin'),
             ('Kokum','Kokum'),
             ('Lime','Lime'),
             ('Macadamia','Macadamia'),
             ('Mahogani','Mahogani'),
             ('Maize','Maize'),
             ('Mango','Mango'),
             ('Mangosteen','Mangosteen'),
             ('Mosambi','Mosambi'),
             ('Nutmeg','Nutmeg'),
             ('Onion','Onion'),
             ('Paddy','Paddy'),
             ('Papaya','Papaya'),
             ('Pepper','Pepper'),
             ('Pineapple','Pine apple'),
             ('Pomegranate','Pomegranate'),
             ('Potato','Potato'),
             ('Rambutan','Rambutan'),
             ('Rose','Rose'),
             ('Rosewood','Rosewood'),
             ('Sapota','Sapota'),
             ('Sugarcane','Sugarcane'),
             ('Tender Coconut','Tender Coconut'),
             ('Tomato','Tomato'),
             ('Tur','Tur'),
             ('Turmeric','Turmeric'),)
	CROPTYPE = (('Short Term','Short Term'),
                ('Perennial','Perennial'))
	CROPSTAGE = (('Early','Early'),
                 ('Growth','Growth'),
                 ('Yield','Yield'))
	VEGETATION_TYPE=(('Grass & Weeds','Grass & Weeds'),
                     ('Woody Vegetation','Woody Vegetation'))
    
	product_category = models.CharField(max_length=500, null=True, blank=True, choices=category)
	product_name = models.CharField(max_length=1000, null=True, blank=True)
	product_image = CloudinaryField(null=True, blank=True)
	crop = models.CharField(max_length=500, null=True, blank=True, choices=CROPS)
	crop_type = models.CharField(max_length=500, null=True, blank=True, choices=CROPTYPE)
	land_extent = models.CharField(max_length=500, null=True, blank=True)
	soil_condition = models.CharField(max_length=500, null=True, blank=True, choices=SOIL)
	price = models.FloatField(null=True, blank=True)
	quality = models.CharField(max_length=200,null=True, blank=True, choices=PRODQUAL)
	brand = models.CharField(max_length=500, null=True, blank=True)
	crop_stage = models.CharField(max_length=200, null=True, blank=True, choices=CROPSTAGE)
	labour_employed = models.CharField(max_length=200, null=True, blank=True)
	max_output = models.CharField(max_length=200,null=True, blank=True)
	fuel_consumption = models.CharField(max_length=500, null=True, blank=True)
	engine_type = models.CharField(max_length=500, null=True, blank=True, choices=FMTYPE)
	fuel_type = models.CharField(max_length=500, null=True, blank=True)
	vegetation_type =models.CharField(max_length=500, choices=VEGETATION_TYPE, null=True,blank=True)
	unit = models.CharField(max_length=200,null=True, blank=True)  
	portability = models.CharField(max_length=200, null=True, blank=True)
	irrigation_solution = models.CharField(max_length=500, null=True, blank=True,choices=IRRISOL)
	irrigation_type = models.CharField(max_length=500, null=True, blank=True,choices=IRRITYPE)
	irrigation_usage = models.CharField(max_length=500, null=True, blank=True,choices=IRRIUSAGE) 
	website_link = models.CharField(max_length=1000, null=True, blank=True)

	class Meta:
		verbose_name = 'AgMachineX: Upload Farm Machinery & Drip Irrigation Specifications'
		verbose_name_plural = 'AgMachineX: Upload Farm Machinery & Drip Irrigation Specifications'

# AgMachineX User Input  -- User
class AgMachineXUserInput(models.Model):
    STAGES = (
        ('Early Stage', 'Early Stage'),
        ('Growth Stage', 'Growth Stage'),
        ('Yield Stage', 'Yield Stage'),
    )

    CATEGORY = (
        ('Irrigation Systems', 'Irrigation Systems'),
        ('Brush Cutter', 'Brush Cutter'),
        ('Power Weeder', 'Power Weeder'),
        ('Power Tiller', 'Power Tiller'),
        ('Water Pump', 'Water Pump'),
        ('Sprayer', 'Sprayer'),
        ('HTP Sprayer', 'HTP Sprayer'),
        ('Earth Auger', 'Earth Auger'),
        ('Chainsaw', 'Chainsaw'),
        ('Hedge Trimmer', 'Hedge Trimmer'),
        ('Chaff Cutter', 'Chaff Cutter'),
        ('Milking Machine', 'Milking Machine'),
        ('Lawn Mower', 'Lawn Mower'),
        ('Generator', 'Generator'),
        ('Engine', 'Engine'),
        ('Sprayer Manual', 'Sprayer Manual'),
        ('Milking Machine Manual', 'Milking Machine Manual'),
        ('Coconut Climber', 'Coconut Climber'),
    )

    SOIL = (
        ('Soft', 'Soft'),
        ('Hard', 'Hard'),
        ('With Stone', 'With Stone'),
    )

    BUDGET = (
        ('Below than Rs. 10000', 'Below than Rs. 10000'),
        ('Between Rs. 10000 to Rs. 20000', 'Between Rs. 10000 to Rs. 20000'),
        ('Between Rs. 20000 to Rs. 50000', 'Between Rs. 20000 to Rs. 50000'),
        ('Between Rs. 50000 to Rs. 1,00,000', 'Between Rs. 50000 to Rs. 1,00,000'),
        ('Between Rs. 1,00,000 to Rs. 1,50,000', 'Between Rs. 1,00,000 to Rs. 1,50,000'),
        ('Between Rs. 1,50,000 to Rs. 2,00,000', 'Between Rs. 1,50,000 to Rs. 2,00,000'),
        ('Between Rs. 2,00,000 to Rs. 2,50,000', 'Between Rs. 2,00,000 to Rs. 2,50,000'),
        ('Above than Rs. 2,50,000', 'Above than Rs. 2,50,000'),
    )

    CROPS = (
        ('Potato', 'Potato'),
        ('Tomato', 'Tomato'),
        ('Banana', 'Banana'),
        ('Sugarcane', 'Sugarcane'),
        ('Coffee', 'Coffee'),
        ('Pepper', 'Pepper'),
        ('Papaya', 'Papaya'),
    )

    IRRITYPE = (
        ('Drip', 'Drip'),
        ('Flood', 'Flood'),
        ('Sprinkler', 'Sprinkler'),
        ('Others', 'Others'),
    )

    IRRIREQ = (
        ('Drip', 'Drip'),
        ('Sprinkler', 'Sprinkler'),
        ('For Fertigation', 'For Fertigation'),
    )

    VEGETATION_TYPE = (
        ('Grass & Weeds', 'Grass & Weeds'),
        ('Woody Vegetation', 'Woody Vegetation'),
    )

    user = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True)
    full_name = models.CharField(max_length=255, null=True, blank=True)
    whatsapp_no = models.CharField(max_length=255, null=True, blank=True)
    email_id = models.CharField(max_length=255, null=True, blank=True)
    village = models.CharField(max_length=255, null=True, blank=True)
    taluk = models.CharField(max_length=500, null=True, blank=True)
    district = models.CharField(max_length=500, null=True, blank=True)
    state = models.CharField(max_length=255, null=True, blank=True)
    zip_code = models.CharField(max_length=255, null=True, blank=True)
    land_area = models.CharField(max_length=100, null=True, blank=True)
    zone = models.CharField(max_length=255, null=True, blank=True)

    soil_condition = models.CharField(max_length=255, choices=SOIL, null=True, blank=True)
    labours_employed = models.CharField(max_length=500, null=True, blank=True)
    crop = models.CharField(max_length=255, choices=CROPS, null=True, blank=True)
    crop_stage = models.CharField(max_length=255, choices=STAGES, null=True, blank=True)

    machinery_req = models.CharField(max_length=500, choices=CATEGORY, null=True, blank=True)
    soil_type = models.CharField(max_length=500, choices=SOIL, null=True, blank=True)
    machine_available = models.CharField(max_length=500, choices=CATEGORY, null=True, blank=True)

    irrigation_type = models.CharField(max_length=500, choices=IRRITYPE, null=True, blank=True)
    water_source = models.CharField(max_length=500, null=True, blank=True)
    water_availability = models.CharField(max_length=500, null=True, blank=True)

    current_irrigation_method = models.CharField(max_length=500, choices=IRRITYPE, null=True, blank=True)
    other_current_irrigation = models.TextField(null=True, blank=True)

    irrigation_req = models.CharField(max_length=500, choices=IRRIREQ, null=True, blank=True)
    budget = models.CharField(max_length=500, choices=BUDGET, null=True, blank=True)
    vegetation_type = models.CharField(max_length=500, choices=VEGETATION_TYPE, null=True, blank=True)

    class Meta:
        verbose_name = 'AgMachinex: Get User Enquiries'
        verbose_name_plural = 'AgMachinex: Get User Enquiries'

    def __str__(self):
        return self.full_name if self.full_name else "Anonymous Submission"


#AgriFBI Stored Data: Crop and Crop Images
class AgriFBI(models.Model):
    CROPS = (('Arecanut','Arecanut'),
             ('Cashew Nut','Cashew Nut'),
             ('Coconut & Copra','Coconut & Copra'),
             ('Coffee','Coffee'),
             ('Cotton','Cotton'),
             ('Maize','Maize'),
             ('Onion','Onion'),
             ('Pepper','Pepper'),
             ('Tomato','Tomato'),
             ('Tur','Tur'))
    crop = models.CharField(max_length=500, choices=CROPS)
    crop_image = CloudinaryField(default='')

    class Meta:
        verbose_name = 'Agri FBI: Upload Crop-Specific Market Prospects Reports'
        verbose_name_plural = 'Agri FBI: Upload Crop-Specific Market Prospects Reports'

#Agri FBI Stored Data: Current Month Report, this model is inline with the AgriFBI
class CurrentMonthReport(models.Model):
    crop = models.ForeignKey(AgriFBI, on_delete=models.CASCADE)
    market_price = models.FloatField(null=True, blank=True)
    crop_trend = CloudinaryField(null=True, blank=True)
    price_outlook = models.CharField(max_length=1000, null=True, blank=True)
    price_outlook_kannada = models.CharField(max_length=1000, null=True, blank=True)
    summary_reviews = models.TextField(null=True, blank=True)
    summary_reviews_kannada = models.TextField(null=True, blank=True)
    bull_bear_factors = models.TextField(null=True, blank=True)
    bull_bear_factors_kannada = models.TextField(null=True, blank=True)
    news = models.TextField(null=True, blank=True)
    news_kannada = models.TextField(null=True, blank=True)
    events = models.TextField(null=True, blank=True)
    events_kannada = models.TextField(null=True, blank=True)
    notifications = models.TextField(null=True, blank=True)
    notifications_kannada = models.TextField(null=True, blank=True)
    farmer_advisor = models.TextField(null=True, blank=True)
    farmer_advisor_kannada = models.TextField(null=True, blank=True)

#Agri FBI Stored Data: Last Month Report, this model is inline with the AgriFBI
class LastMonthReport(models.Model):
    crop = models.ForeignKey(AgriFBI, related_name='last_month_report', on_delete=models.CASCADE, default='')
    price_outlook = models.TextField(null=True, blank=True)
    price_outlook_kannada = models.TextField(null=True, blank=True)
    bull_bear_factors = models.TextField(null=True, blank=True)
    bull_bear_factors_kannada = models.TextField(null=True, blank=True)
    user_feedback = models.TextField(null=True, blank=True)
    user_feedback_kannada = models.TextField(null=True, blank=True)

#Agri FBI Stored Data: Seasonal Month Report, this model is inline with the AgriFBI
class SeasonalReport(models.Model):
    crop = models.ForeignKey(AgriFBI, related_name='seasonal_report', on_delete=models.CASCADE, default='')
    price_outlook = models.TextField(null=True, blank=True)
    price_outlook_kannada = models.TextField(null=True, blank=True)
    summary_reviews = models.TextField(null=True, blank=True)
    summary_reviews_kannada = models.TextField(null=True, blank=True)
    bull_bear_factors = models.TextField(null=True, blank=True)
    bull_bear_factors_kannada = models.TextField(null=True, blank=True)

#Agri FBI User Enquiries
class FBIEnquiry(models.Model):
    user_name = models.CharField(max_length=500, null=True)
    phone_no = models.CharField(max_length=10, null=True)
    crop = models.CharField(max_length=255)

    class Meta:
        verbose_name = 'Agri FBI: Get User Enquiries'
        verbose_name_plural = 'Agri FBI: Get User Enquiries'

#Agri FBI Market Planner: User Response for Fund Requirement Model
class FundRequirement(models.Model):
    CROPS = (('',''),
             ('Arecanut','Arecanut'),
             ('Cashew Nut','Cashew Nut'),
             ('Coconut & Copra','Coconut & Copra'),
             ('Coffee','Coffee'),
             ('Cotton','Cotton'),
             ('Maize','Maize'),
             ('Onion','Onion'),
             ('Pepper','Pepper'),
             ('Tomato','Tomato'),
             ('Tur','Tur'))
    VARIETIES = (('',''),
                 ('Hirehalli local','Hirehalli local'),
                 ('Tumkur local','Tumkur local'),
                 ('Mohith Nagar','Mohith Nagar'),
                 ('Sirsi local','Sirsi local'),
                 ('Tirthahalli Local','Tirthahalli Local'),
                 ('Sagar Local','Sagar Local'),
                 ('Sumangala','Sumangala'),
                 ('Mangala','Mangala'),
                 ('Tiptur','Tiptur'),
                 ('Arasikere tall','Arasikere tall'),
                 ('West coast tall','West coast tall'),
                 ('Arabica','Robusta'),
                 ('V-4','V-4'),
                 ('V-7','V-7'),
                 ('Bhaskara','Bhaskara'),
                 ('Ullal-1','Ullal-1'),
                 ('Ullal-5','Ullal-5'),
                 ('Panniyur -1','Panniyur -1'),
                 ('Panniyur -2','Panniyur -2'),
                 ('Panniyur -3','Panniyur -3'),
                 ('Kari maligge sara','Kari maligge sara'))
    user_type = models.CharField(max_length=500, default='')
    name = models.CharField(max_length=500,default='')
    phone_no = models.CharField(max_length=10,default='')
    email = models.EmailField(null=True, blank=True)
    state = models.CharField(max_length=500,default='')
    district = models.CharField(max_length=500, null=True, blank=True)
    taluk = models.CharField(max_length=500, null=True, blank=True)
    village = models.CharField(max_length=255, null=True, blank=True)
    zone = models.CharField(max_length=255, null=True, blank=True)
    zip_code = models.CharField(max_length=255, default='')
    crops = models.CharField(max_length=255, choices=CROPS)
    crop_varieties = models.CharField(max_length=255, choices=VARIETIES)
    quantity_available = models.CharField(max_length=255, default='')
    amount_jan = models.CharField(max_length=255, null=True, blank=True)
    amount_feb = models.CharField(max_length=255,  null=True, blank=True)
    amount_mar = models.CharField(max_length=255,  null=True, blank=True)
    amount_apr = models.CharField(max_length=255, null=True, blank=True)
    amount_may = models.CharField(max_length=255, null=True, blank=True)
    amount_jun = models.CharField(max_length=255, null=True, blank=True)
    amount_jul = models.CharField(max_length=255, null=True, blank=True)
    amount_aug = models.CharField(max_length=255, null=True, blank=True)
    amount_sep = models.CharField(max_length=255, null=True, blank=True)
    amount_oct = models.CharField(max_length=255, null=True, blank=True)
    amount_nov = models.CharField(max_length=255, null=True, blank=True)
    amount_dec = models.CharField(max_length=255, null=True, blank=True)

    class Meta:
        verbose_name = 'Agri FBI Market Planner: Get User Fund Requirement Enquiries'
        verbose_name_plural = 'Agri FBI Market Planner: Get User Fund Requirement Enquiries'

#Agri FBI Market Planner: User Response for Quantity Requirement Model
class QtyRequirement(models.Model):
    CROPS = (('',''),
             ('Arecanut','Arecanut'),
             ('Cashew Nut','Cashew Nut'),
             ('Coconut & Copra','Coconut & Copra'),
             ('Coffee','Coffee'),
             ('Cotton','Cotton'),
             ('Maize','Maize'),
             ('Onion','Onion'),
             ('Pepper','Pepper'),
             ('Tomato','Tomato'),
             ('Tur','Tur'))
    VARIETIES = (('',''),
                 ('Hirehalli local','Hirehalli local'),
                 ('Tumkur local','Tumkur local'),
                 ('Mohith Nagar','Mohith Nagar'),
                 ('Sirsi local','Sirsi local'),
                 ('Tirthahalli Local','Tirthahalli Local'),
                 ('Sagar Local','Sagar Local'),
                 ('Sumangala','Sumangala'),
                 ('Mangala','Mangala'),
                 ('Tiptur','Tiptur'),
                 ('Arasikere tall','Arasikere tall'),
                 ('West coast tall','West coast tall'),
                 ('Arabica','Robusta'),
                 ('V-4','V-4'),
                 ('V-7','V-7'),
                 ('Bhaskara','Bhaskara'),
                 ('Ullal-1','Ullal-1'),
                 ('Ullal-5','Ullal-5'),
                 ('Panniyur -1','Panniyur -1'),
                 ('Panniyur -2','Panniyur -2'),
                 ('Panniyur -3','Panniyur -3'),
                 ('Kari maligge sara','Kari maligge sara'))
    user_type = models.CharField(max_length=500, default='')
    name = models.CharField(max_length=500,default='')
    phone_no = models.CharField(max_length=10,default='')
    email = models.EmailField(null=True, blank=True)
    state = models.CharField(max_length=500,default='')
    district = models.CharField(max_length=500, null=True, blank=True)
    taluk = models.CharField(max_length=500, null=True, blank=True)
    village = models.CharField(max_length=255, null=True, blank=True)
    zone = models.CharField(max_length=255, null=True, blank=True)
    zip_code = models.CharField(max_length=255, default='')
    crops = models.CharField(max_length=255, choices=CROPS)
    crop_varieties = models.CharField(max_length=255, choices=VARIETIES)
    quantity_required = models.CharField(max_length=255, default='')
    amount_jan = models.CharField(max_length=255, null=True, blank=True)
    amount_feb = models.CharField(max_length=255,  null=True, blank=True)
    amount_mar = models.CharField(max_length=255,  null=True, blank=True)
    amount_apr = models.CharField(max_length=255, null=True, blank=True)
    amount_may = models.CharField(max_length=255, null=True, blank=True)
    amount_jun = models.CharField(max_length=255, null=True, blank=True)
    amount_jul = models.CharField(max_length=255, null=True, blank=True)
    amount_aug = models.CharField(max_length=255, null=True, blank=True)
    amount_sep = models.CharField(max_length=255, null=True, blank=True)
    amount_oct = models.CharField(max_length=255, null=True, blank=True)
    amount_nov = models.CharField(max_length=255, null=True, blank=True)
    amount_dec = models.CharField(max_length=255, null=True, blank=True)

    class Meta:
        verbose_name = 'Agri FBI Market Planner: Get User Quantity Requirement Enquiries'
        verbose_name_plural = 'Agri FBI Market Planner: Get User Quantity Requirement Enquiries'

#Agri FBI Market Planner: User Response for Actual Sales Model
class ActualSales(models.Model):
    CROPS = (('',''),
             ('Arecanut','Arecanut'),
             ('Cashew Nut','Cashew Nut'),
             ('Coconut & Copra','Coconut & Copra'),
             ('Coffee','Coffee'),
             ('Cotton','Cotton'),
             ('Maize','Maize'),
             ('Onion','Onion'),
             ('Pepper','Pepper'),
             ('Tomato','Tomato'),
             ('Tur','Tur'))
    VARIETIES = (('',''),
                 ('Hirehalli local','Hirehalli local'),
                 ('Tumkur local','Tumkur local'),
                 ('Mohith Nagar','Mohith Nagar'),
                 ('Sirsi local','Sirsi local'),
                 ('Tirthahalli Local','Tirthahalli Local'),
                 ('Sagar Local','Sagar Local'),
                 ('Sumangala','Sumangala'),
                 ('Mangala','Mangala'),
                 ('Tiptur','Tiptur'),
                 ('Arasikere tall','Arasikere tall'),
                 ('West coast tall','West coast tall'),
                 ('Arabica','Robusta'),
                 ('V-4','V-4'),
                 ('V-7','V-7'),
                 ('Bhaskara','Bhaskara'),
                 ('Ullal-1','Ullal-1'),
                 ('Ullal-5','Ullal-5'),
                 ('Panniyur -1','Panniyur -1'),
                 ('Panniyur -2','Panniyur -2'),
                 ('Panniyur -3','Panniyur -3'),
                 ('Kari maligge sara','Kari maligge sara'))
    name = models.CharField(max_length=500,default='')
    phone_no = models.CharField(max_length=10,default='')
    email = models.EmailField(null=True, blank=True)
    state = models.CharField(max_length=500,default='')
    district = models.CharField(max_length=500, null=True, blank=True)
    taluk = models.CharField(max_length=500, null=True, blank=True)
    village = models.CharField(max_length=255, null=True, blank=True)
    zone = models.CharField(max_length=255, null=True, blank=True)
    zip_code = models.CharField(max_length=255, default='')
    land_area = models.CharField(max_length=100, null=True, blank=True)
    crops = models.CharField(max_length=255, choices=CROPS)
    crop_varieties = models.CharField(max_length=255, choices=VARIETIES)
    amount_jan = models.CharField(max_length=255, null=True, blank=True)
    amount_feb = models.CharField(max_length=255,  null=True, blank=True)
    amount_mar = models.CharField(max_length=255,  null=True, blank=True)
    amount_apr = models.CharField(max_length=255, null=True, blank=True)
    amount_may = models.CharField(max_length=255, null=True, blank=True)
    amount_jun = models.CharField(max_length=255, null=True, blank=True)
    amount_jul = models.CharField(max_length=255, null=True, blank=True)
    amount_aug = models.CharField(max_length=255, null=True, blank=True)
    amount_sep = models.CharField(max_length=255, null=True, blank=True)
    amount_oct = models.CharField(max_length=255, null=True, blank=True)
    amount_nov = models.CharField(max_length=255, null=True, blank=True)
    amount_dec = models.CharField(max_length=255, null=True, blank=True)
    quant_jan = models.CharField(max_length=255, null=True, blank=True)
    quant_feb = models.CharField(max_length=255, null=True, blank=True)
    quant_mar = models.CharField(max_length=255, null=True, blank=True)
    quant_apr = models.CharField(max_length=255, null=True, blank=True)
    quant_may = models.CharField(max_length=255, null=True, blank=True)
    quant_jun = models.CharField(max_length=255, null=True, blank=True)
    quant_jul = models.CharField(max_length=255, null=True, blank=True)
    quant_aug = models.CharField(max_length=255, null=True, blank=True)
    quant_sep = models.CharField(max_length=255, null=True, blank=True) 
    quant_oct = models.CharField(max_length=255, null=True, blank=True)
    quant_nov = models.CharField(max_length=255, null=True, blank=True)
    quant_dec = models.CharField(max_length=255, null=True, blank=True)

    class Meta:
        verbose_name = 'Agri FBI Market Planner: Get User Actual Sales Enquiries'
        verbose_name_plural = 'Agri FBI Market Planner: Get User Actual Sales Enquiries'

#Agri FBI Market Planner Stored Data:Uploading Monthly Price Outlook 
class MarketPlannerStrategy(models.Model):
    CROPS = (('',''),
             ('Arecanut','Arecanut'),
             ('Cashew Nut','Cashew Nut'),
             ('Coconut & Copra','Coconut & Copra'),
             ('Coffee','Coffee'),
             ('Cotton','Cotton'),
             ('Maize','Maize'),
             ('Onion','Onion'),
             ('Pepper','Pepper'),
             ('Tomato','Tomato'),
             ('Tur','Tur'))
    VARIETIES = (('',''),
                 ('Hirehalli local','Hirehalli local'),
                 ('Tumkur local','Tumkur local'),
                 ('Mohith Nagar','Mohith Nagar'),
                 ('Sirsi local','Sirsi local'),
                 ('Tirthahalli Local','Tirthahalli Local'),
                 ('Sagar Local','Sagar Local'),
                 ('Sumangala','Sumangala'),
                 ('Mangala','Mangala'),
                 ('Tiptur','Tiptur'),
                 ('Arasikere tall','Arasikere tall'),
                 ('West coast tall','West coast tall'),
                 ('Arabica','Robusta'),
                 ('V-4','V-4'),
                 ('V-7','V-7'),
                 ('Bhaskara','Bhaskara'),
                 ('Ullal-1','Ullal-1'),
                 ('Ullal-5','Ullal-5'),
                 ('Panniyur -1','Panniyur -1'),
                 ('Panniyur -2','Panniyur -2'),
                 ('Panniyur -3','Panniyur -3'),
                 ('Kari maligge sara','Kari maligge sara'))
    INDICATORS = (('1. High Inflation (Positive Trending)','1. High Inflation (Positive Trending)'),
                  ('2. Elevated risk of price escalation (Positive Movement)','2. Elevated risk of price escalation (Positive Movement)'),
                  ('3. Price Convergence (High Spread)','3. Price Convergence (High Spread)'),
                  ('4. Potential risk of Decline(Negative Movement)','4. Potential risk of Decline(Negative Movement'),
                  ('5. Sharp Decline (Negative Trending)','5. Sharp Decline (Negative Trending)'))
    upload_excel = CloudinaryField(resource_type='auto')
    crops = models.CharField(max_length=255, choices=CROPS)
    crop_varieties = models.CharField(max_length=255, choices=VARIETIES)
    price_outlook_jan = models.CharField(max_length=500, choices=INDICATORS, null=True, blank=True)
    price_outlook_feb = models.CharField(max_length=500, choices=INDICATORS, null=True, blank=True)
    price_outlook_mar = models.CharField(max_length=500, choices=INDICATORS, null=True, blank=True)
    price_outlook_apr = models.CharField(max_length=500, choices=INDICATORS, null=True, blank=True)
    price_outlook_may = models.CharField(max_length=500, choices=INDICATORS, null=True, blank=True)
    price_outlook_jun = models.CharField(max_length=500, choices=INDICATORS, null=True, blank=True)
    price_outlook_jul = models.CharField(max_length=500, choices=INDICATORS, null=True, blank=True)
    price_outlook_aug = models.CharField(max_length=500, choices=INDICATORS, null=True, blank=True)
    price_outlook_sep = models.CharField(max_length=500, choices=INDICATORS, null=True, blank=True)
    price_outlook_oct = models.CharField(max_length=500, choices=INDICATORS, null=True, blank=True)
    price_outlook_nov = models.CharField(max_length=500, choices=INDICATORS, null=True, blank=True)
    price_outlook_dec = models.CharField(max_length=500, choices=INDICATORS, null=True, blank=True)

    def __str__(self):
        return self.crops
    
    class Meta:
        verbose_name = 'Agri FBI Market Planner: Upload Monthly Crop-Specific Price Outlooks'
        verbose_name_plural = 'Agri FBI Market Planner: Upload Monthly Crop-Specific Price Outlooks'

#CropIntel Stored Data
class CropIntelKnowledge(models.Model):
	CROPS = (('Amla','Amla'),
             ('Areca New', 'Areca New'),
             ('Arecanut', 'Arecanut'),
             ('Avocado','Avocado'),
             ('Banana', 'Banana'),
             ('Betelvine','Betelvine'),
             ('Cashewnut','Cashewnut'),
             ('Cocoa','Cocoa'),
             ('Coconut','Coconut'),
             ('Coffee','Coffee'),
             ('Curry leaves','Curry leaves'),
             ('Custard apple','Custard apple'),
             ('Dragon fruit','Dragon fruit'),
             ('Drumstick','Drumstick'),
             ('Durian','Durian'),
             ('Fig','Fig'),
             ('Grapes','Grapes'),
             ('Guava','Guava'),
             ('Jack Fruit','Jack Fruit'),
             ('Jasmin','Jasmin'),
             ('Kokum','Kokum'),
             ('Lime','Lime'),
             ('Macadamia','Macadamia'),
             ('Mahogani','Mahogani'),
             ('Mango','Mango'),
             ('Mangosteen','Mangosteen'),
             ('Mosambi','Mosambi'),
             ('Nutmeg','Nutmeg'),
             ('Papaya','Papaya'),
             ('Pepper','Pepper'),
             ('Pineapple','Pineapple'),
             ('Pomegranate','Pomegranate'),
             ('Rambutan','Rambutan'),
             ('Rosewood','Rosewood'),
             ('Sapota','Sapota'),
             ('Tender Coconut','Tender Coconut'))
	'''VARIETIES = (('NA-7','NA-7'),
                 ('Krishna','Krishna'),
                 ('Kanchana','Kanchana'),
                 ('Chakiya','Chakiya'),
                 ('Mangalore White Chali','Mangalore White Chali'),
                 ('Shimoga','Shimoga'),
                 ('Davanagere Api','Davanagere Api'),
                 ('Chikkamagalore Saraku','Chikkamagalore Saraku'),
                 ('North kanara rashi','North kanara rashi'),
                 ('Hirehalli local','Hirehalli local'),
                 ('Tumkur local','Tumkur local'),
                 ('Mohith Nagar','Mohith Nagar'),
                 ('Sirsi local','Sirsi local'),
                 ('Tirthahalli Local','Tirthahalli Local'),
                 ('Sagar Local','Sagar Local'),
                 ('Sumangala','Sumangala'),
                 ('Mangala','Mangala'),
                 ('Hass','Hass'),
                 ('Florida gold','Florida gold'),
                 ('Green gold','Green gold'),
                 ('Kaveri grand','Kaveri grand'),
                 ('B N grand','B N grand'),
                 ('B G S grand','B G S grand'),
                 ('G9','G9'),
                 ('Yellaki','Yellaki'),
                 ('Nendran','Nendran'),
                 ('Mysoreale','Mysoreale'),
                 ('Kariyale','Kariyale'),
                 ('Ambudiale','Ambudiale'),
                 ('V-4','V-4'),
                 ('V-7','V-7'),
                 ('Bhaskara','Bhaskara'),
                 ('Ullal-1','Ullal-1'),
                 ('Ullal-5','Ullal-5'),
                 ('Criollo','Criollo'),
                 ('Trinitario','Trinitario'),
                 ('Forastero','Forastero'),
                 ('Tiptur','Tiptur'),
                 ('Arasikere tall','Arasikere tall'),
                 ('West coast tall','West coast tall'),
                 ('Arabica','Arabica'),
                 ('Sen kaampa','Sen kaampa'),
                 ('Dharwad-1','Dharwad-1'),
                 ('Dharwad-2','Dharwad-2'),
                 ('Gamthi','Gamthi'),
                 ('NMK-1 Golden','NMK-1 Golden'),
                 ('White Dragon -1','White Dragon -1'),
                 ('Jumbo red dragon -1','Jumbo red dragon -1'),
                 ('Pink dragon','Pink dragon'),
                 ('Rohith-1','Rohith-1'),
                 ('Coimbature-2','Coimbature-2'),
                 ('PKM-1','PKM-1'),
                 (' PKM-2','PKM-2'),
                 ('Mornthong','Mornthong'),
                 ('Chanee','Chanee'),
                 ('Kani','Kani'),
                 ('Brown turkey','Brown turkey'),
                 ('Puna Fig','Puna Fig'),
                 ('Thompson seedless','Thompson seedless'),
                 ('Sharad seedless','Sharad seedless'),
                 ('Red globe','Red globe'),
                 ('Dilkush','Dilkush'),
                 ('Blanc du Bois','Blanc du Bois'),
                 ('Sonaka seedless','Sonaka seedless'),
                 ('Tas-e-ganesh','Tas-e-ganesh'),
                 ('Allahabad safeda guava','Allahabad safeda guava'),
                 ('Dimond seedless','Dimond seedless'),
                 ('Thai white seedless','Thai white seedless'),
                 ('Siddu variety','Siddu variety'),
                 ('Khaja variety','Khaja variety'),
                 ('Rudrakshi','Rudrakshi'),
                 ('Mysuru mallige','Mysuru mallige'),
                 ('Udupi mallige','Udupi mallige'),
                 ('Konkan Amritha','Konkan Amritha'),
                 ('Balaji','Balaji'),
                 ('Kaggzi lemon','Kaggzi lemon'),
                 ('Gol nemu','Gol nemu'),
                 ('Macadamia integrifolia','Macadamia integrifolia'),
                 ('Macadamia tetraphylla','Macadamia tetraphylla'),
                 ('Forest spp','Forest spp'),
                 ('Alphenso','Alphenso'),
                 ('Malgova','Malgova'),
                 ('Raspuri','Raspuri'),
                 ('Bensha','Bensha'),
                 ('Kesar','Kesar'),
                 ('Mallika','Mallika'),
                 ('Totapuri','Totapuri'),
                 ('Neelam','Neelam'),
                 ('Seashore mangosteen','Seashore mangosteen'),
                 ('Sathgudi','Sathgudi'),
                 ('Viswasree','Viswasree'),
                 ('Keralashree','Keralashree'),
                 ('Red lady','Red lady'),
                 ('Panniyur -1','Panniyur -1'),
                 ('Panniyur -2','Panniyur -2'),
                 ('Panniyur -3','Panniyur -3'),
                 ('Kari maligge sara','Kari maligge sara'),
                 ('Queen','Queen'),
                 ('Kew','Kew'),
                 ('Bhagwa','Bhagwa'),
                 ('Ganesh','Ganesh'),
                 ('Mridula(Arakta)','Mridula(Arakta)'),
                 ('Ruby','Ruby'),
                 ('Arka Coorg Arun (Red colour)','Arka Coorg Arun (Red colour)'),
                 ('Arka Coorg Peetabh (yellow colour)','Arka Coorg Peetabh (yellow colour)'),
                 ('Indian Rosewood','Indian Rosewood'),
                 ('Bahia Rosewood','Bahia Rosewood'),
                 ('Cricket Ball','Cricket Ball'),
                 ('Kalipatti','Kalipatti'),
                 ('DHS-1','DHS-1'),
                 ('DHS-2','DHS-2'),
                 ('chowghat orange drawf','chowghat orange drawf'),
                 ('Malayan Yellow Drawf','Malayan Yellow Drawf'),
                 ('Ganga Bondum','Ganga Bondum'))'''
	
	ZONES = (('Plain-North Zone','Plain-North Zone'),
             ('Plain-South Zone','Plain-South Zone'),
             ('Coastal Zone','Coastal Zone'),
             ('Western (Malenadu) Zone','Western (Malenadu) Zone'))
	PROPAGATION = (('Budding','Budding'),
                   ('Softwood Grafting','Softwood Grafting'),
                   ('Seeds','Seeds'),
                   ('Cuttings','Cuttings'),
                   ('Layering','Layering'),
                   ('Grafting','Grafting'),
                   ('Suckers','Suckers'),
                   ('Tissue Culture','Tissue Culture'),
                   ('Air Layering','Air Layering'),
                   ('Epicotyl Grafting','Epicotyl Grafting'),
                   ('Nuts','Nuts'),
                   ('Stem Cuttings','Stem Cuttings'),
                   ('Micropropagation','Micropropagation'),
                   ('Blossoming','Blossoming'),
                   ('Bud Grafting','Bud Grafting'),
                   ('Shoot Cuttings','Shoot Cuttings'),)
	SOIL_TYPES = (('Sandy loam','Sandy loam'),
                  ('Loamy Soil','Loamy Soil'),
                  ('Black Soil','Black Soil'),
                  ('Red Sandy Loam','Red Sandy Loam'),
                  ('Lateritic Soil','Lateritic Soil'),
                  ('Clay Loam Soil','Clay Loam Soil'),
                  ('Red Lateritic Soil','Red Lateritic Soil'),
                  ('Alluvial Clay','Alluvial Clay'),
                  ('Coastal Alluvial Soil','Coastal Alluvial Soil'),
                  ('Red Loamy Soil', 'Red Loamy Soil'),
                  ('Mountainous Soil','Mountainous Soil'),
                  ('Silt Loamy Soil','Silt Loamy Soil'),)
	INDICATORS = (('1. High Inflation (Positive Trending)','1. High Inflation (Positive Trending)'),
                  ('2. Elevated risk of price escalation (Positive Movement)','2. Elevated risk of price escalation (Positive Movement)'),
                  ('3. Price Convergence (High Spread)','3. Price Convergence (High Spread)'),
                  ('4. Potential risk of Decline(Negative Movement)','4. Potential risk of Decline(Negative Movement'),
                  ('5. Sharp Decline (Negative Trending)','5. Sharp Decline (Negative Trending)'))
	WATER_SUFFICIENCIES = (('Very Good Water Availability','Very Good Water Availability'),
                           ('Good Water Availability','Good Water Availability'),
                           ('Average Water Availability','Average Water Availability'),
                           ('Limited Water Availability','Limited Water Availability'),
                           ('Poor Water Availability','Poor Water Availability'))
	INTERCROPS = (('Acacia', 'Acacia'),
                ('Avocado', 'Avocado'),
                ('Banana', 'Banana'),
                ('Cardamom', 'Cardamom'),
                ('Cashew Nut', 'Cashew Nut'),
                ('Cocoa', 'Cocoa'),
                ('Coconut', 'Coconut'),
                ('Coffee', 'Coffee'),
                ('Citrus', 'Citrus'),
                ('Drumstick', 'Drumstick'),
                ('Dwarf sapota', 'Dwarf sapota'),
                ('Fig', 'Fig'),
                ('Ginger', 'Ginger'),
                ('Guava', 'Guava'),
                ('Lime', 'Lime'),
                ('Macadamia', 'Macadamia'),
                ('Mahogany', 'Mahogany'),
                ('Medium term crops', 'Medium term crops'),
                ('NA', 'NA'),
                ('Nutmeg', 'Nutmeg'),
                ('Other Fruits Crops', 'Other Fruits Crops'),
                ('Papaya', 'Papaya'),
                ('Pineapple', 'Pineapple'),
                ('Pomegranate', 'Pomegranate'),
                ('Rubber', 'Rubber'),
                ('Sandalwood', 'Sandalwood'),
                ('Teak', 'Teak'))

	crop = models.CharField(max_length=500, choices=CROPS)
	#crop_varieties = models.CharField(max_length=500, choices=VARIETIES, default='')
	selected_crop_varieties = models.CharField(max_length=1000, null=True, blank=True)
	crop_variety_image = CloudinaryField(default='')
	market_prospects = models.TextField(null=True, blank=True, choices=INDICATORS)
	current_month_report = models.TextField(null=True, blank=True)
	seasonal_report = models.TextField(null=True, blank=True)
	#historical_report = models.TextField(null=True, blank=True)
	propagation_method = MultiSelectField(choices=PROPAGATION, max_choices=4, max_length=255, default='')
	yield_potential = models.CharField(null=True, blank=True, max_length=255)
	economical_yield_start = models.CharField(null=True, blank=True, max_length=255)
	ideal_age_planting = models.CharField(null=True, blank=True, max_length=255)
	harvest = models.CharField(null=True, blank=True, max_length=255)
	area_zone = MultiSelectField(choices=ZONES, max_choices=4, max_length=255, default='')
	soil_pH = models.CharField(null=True, blank=True, max_length=255)
	soil_type = MultiSelectField(choices=SOIL_TYPES, max_choices=4, max_length=255, default='')
	water_req = models.CharField(choices=WATER_SUFFICIENCIES,null=True, blank=True, max_length=255)
	inter_crop_space = models.CharField(null=True, blank=True, max_length=255)
	recommend_space = models.CharField(null=True, blank=True, max_length=255)
	inter_crops = MultiSelectField(choices=INTERCROPS,max_choices=10,max_length=255,default='')
	selected_intercrops = models.CharField(max_length=1000, null=True, blank=True)
	cover_crops = models.CharField(null=True, blank=True, max_length=255)
	manure = models.CharField(null=True, blank=True, max_length=255)
	high_density = models.CharField(null=True, blank=True, max_length=255)
	favorable_temp = models.CharField(null=True, blank=True, max_length=255)
	relative_humidity = models.CharField(null=True, blank=True, max_length=255)
	rainfall_req = models.CharField(null=True, blank=True, max_length=255)
	wind_velocity = models.CharField(null=True, blank=True, max_length=255)
	mean_sea_level = models.CharField(null=True, blank=True, max_length=255)
	location = models.CharField(max_length=1000, null=True, blank=True)

	class Meta:
		verbose_name = 'CropIntel: Upload CropIntel Knowledge data'
		verbose_name_plural = 'CropIntel: Upload CropIntel Knowledge data'

	def __str__(self):
		return self.crop

class CropIntelInput(models.Model):
    LANDS = (('New Land', 'New Land'),
             ('Existing Land', 'Existing Land'))
    
    STAGES = (('Young', 'Young'),
              ('Yielding', 'Yielding'),
              ('Old', 'Old'))
    
    CROPS = (('Amla', 'Amla'),
             ('Areca New', 'Areca New'),
             ('Arecanut', 'Arecanut'),
             ('Avocado', 'Avocado'),
             ('Banana', 'Banana'),
             ('Betelvine', 'Betelvine'),
             ('Cashewnut', 'Cashewnut'),
             ('Cocoa', 'Cocoa'),
             ('Coconut', 'Coconut'),
             ('Coffee', 'Coffee'),
             ('Curry leaves', 'Curry leaves'),
             ('Custard apple', 'Custard apple'),
             ('Dragon fruit', 'Dragon fruit'),
             ('Drumstick', 'Drumstick'),
             ('Durian', 'Durian'),
             ('Fig', 'Fig'),
             ('Grapes', 'Grapes'),
             ('Guava', 'Guava'),
             ('Jack Fruit', 'Jack Fruit'),
             ('Jasmin', 'Jasmin'),
             ('Kokum', 'Kokum'),
             ('Lime', 'Lime'),
             ('Macadamia', 'Macadamia'),
             ('Mahogani', 'Mahogani'),
             ('Mango', 'Mango'),
             ('Mangosteen', 'Mangosteen'),
             ('Mosambi', 'Mosambi'),
             ('Nutmeg', 'Nutmeg'),
             ('Papaya', 'Papaya'),
             ('Pepper', 'Pepper'),
             ('Pineapple', 'Pineapple'),
             ('Pomegranate', 'Pomegranate'),
             ('Rambutan', 'Rambutan'),
             ('Rosewood', 'Rosewood'),
             ('Sapota', 'Sapota'),
             ('Tender Coconut', 'Tender Coconut'))
    
    VARIETIES = (('NA-7', 'NA-7'),
                 ('NA-10', 'NA-10'),
                 ('Chakaiya', 'Chakaiya'),
                 ('Kanchan', 'Kanchan'),
                 ('Fuerte', 'Fuerte'),
                 ('Pinkerton', 'Pinkerton'),
                 ('Hass & Reed', 'Hass & Reed'),
                 ('ICRI 2', 'ICRI 2'),
                 ('IISR Suvarna', 'IISR Suvarna'),
                 ('Malabar', 'Malabar'),
                 ('Mudigere-1', 'Mudigere-1'),
                 ('V-4', 'V-4'),
                 ('Bhaskara', 'Bhaskara'),
                 ('Ullal-1', 'Ullal-1'),
                 ('Ullal-5', 'Ullal-5'),
                 ('Criollo', 'Criollo'),
                 ('Trinitario', 'Trinitario'),
                 ('Forastero', 'Forastero'),
                 ('Chowghat GD', 'Chowghat GD'),
                 ('Chowghat OD', 'Chowghat OD'),
                 ('West CT', 'West CT'),
                 ('Arabica', 'Robusta'),
                 ('Local Landrace Variety', 'Local Landrace Variety'),
                 ('White Dragon-1', 'White Dragon-1'),
                 ('Red dragon-1', 'Red dragon-1'),
                 ('PKM-1', 'PKM-1'),
                 ('Bhagya', 'Bhagya'),
                 ('Trichy-1', 'Trichy-1'),
                 ('Seedless- Thomson', 'Seedless- Thomson'),
                 ('Sharad & Sonaka', 'Sharad & Sonaka'),
                 ('Red globe', 'Red globe'),
                 ('Allahabad Safeda', 'Allahabad Safeda'),
                 ('Varikka', 'Varikka'),
                 ('Idukki Gold', 'Idukki Gold'),
                 ('Muttom Varikka', 'Muttom Varikka'),
                 ('Bangalore Purple', 'Bangalore Purple'),
                 ('Guthi', 'Guthi'),
                 ('Eureka', 'Eureka'),
                 ('Lisbon', 'Lisbon'),
                 ('Meyer', 'Meyer'),
                 ('Macadamia Integrifolia', 'Macadamia Integrifolia'),
                 ('Macadamia Tetraphylla', 'Macadamia Tetraphylla'),
                 ('Forest spp', 'Forest spp'),
                 ('Alphenso', 'Alphenso'),
                 ('Raspuri', 'Raspuri'),
                 ('Mallika', 'Mallika'),
                 ('Totapuri', 'Totapuri'),
                 ('Neelam', 'Neelam'),
                 ('Viswasree', 'Viswasree'),
                 ('Keralashree', 'Keralashree'),
                 ('Dura', 'Dura'),
                 ('Tenera', 'Tenera'),
                 ('Pisifera', 'Pisifera'),
                 ('Panniyur-1', 'Panniyur-1'),
                 ('Subhakara', 'Subhakara'),
                 ('Panniyur-2', 'Panniyur-2'),
                 ('Aimpiriyan', 'Aimpiriyan'),
                 ('Bhagwa', 'Bhagwa'),
                 ('Ganesh', 'Ganesh'),
                 ('Mridula', 'Mridula'),
                 ('Ruby', 'Ruby'),
                 ('Cricket Ball', 'Cricket Ball'),
                 ('Kalipatti', 'Kalipatti'),
                 ('DHS-1', 'DHS-1'),
                 ('DHS-2', 'DHS-2'),
                 ('Indian Teak wood', 'Indian Teak wood'))
    
    LAND_PREPARATION = (('Leveling', 'Leveling'),
                       ('Clearing bushes', 'Clearing bushes'),
                       ('Removing stones', 'Removing stones'))
    
    PESTS = (('Spindle bug', 'Spindle bug'),
             ('Root grub', 'Root grub'),
             ('Infloresence caterpillar', 'Infloresence caterpillar'),
             ('Cholam or white mites', 'Cholam or white mites'))
    
    DISEASES = (('Leaf spot', 'Leaf spot'),
                ('Fruit rot/Koleroga', 'Fruit rot/Koleroga'),
                ('Bud rot', 'Bud rot'),
                ('Yellow leaf disease', 'Yellow leaf disease'),
                ('Infloresence die-back', 'Infloresence die-back'),
                ('Foot rot or Anabe roga', 'Foot rot or Anabe roga'))
    
    PLANTING_METHOD = (('Intercrop', 'Intercrop'),
                       ('Multicrop', 'Multicrop'),
                       ('Monocrop', 'Monocrop'))
    
    # Generate month-year combinations
    current_year = datetime.date.today().year
    start_year = current_year - 10
    end_year = current_year
    years = [str(year) for year in range(start_year, end_year + 1)]
    months = [calendar.month_abbr[i] for i in range(1, 13)]
    month_year = [(f'{month}/{year}', f'{month}/{year}') for year, month in itertools.product(years, months)]
    
    # User information
    user_name = models.CharField(max_length=500, default='')
    phone_no = models.CharField(max_length=10, default='')
    district = models.CharField(max_length=255, default='', blank=True, null=True)
    taluk = models.CharField(max_length=255, default='', blank=True, null=True)
    address = models.CharField(max_length=500, default='', blank=True, null=True)
    
    # Plot information
    plot_name = models.CharField(max_length=500, default='')
    crop_grown = models.CharField(max_length=500, blank=True, null=True, choices=CROPS)
    land_area = models.CharField(max_length=100, blank=True, null=True)
    
    # Soil information
    soil_condition = models.CharField(max_length=255, blank=True, null=True)
    soil_health = models.CharField(max_length=255, blank=True, null=True)
    soil_ph = models.CharField(max_length=255, blank=True, null=True) 
    soil_rich_nutrients = models.CharField(max_length=255, blank=True, null=True)
    soil_average_nutrients = models.CharField(max_length=255, blank=True, null=True)
    soil_poor_nutrients = models.CharField(max_length=255, blank=True, null=True)
    
    # Water information
    water_source = models.CharField(max_length=255, blank=True, null=True)
    water_availability = models.CharField(max_length=255, blank=True, null=True)
    
    # Cultivation details
    land_type = models.CharField(max_length=500, choices=LANDS)
    crop_varieties = models.CharField(max_length=255, null=True, blank=True, choices=VARIETIES)
    no_of_plants = models.CharField(max_length=10, default='', null=True, blank=True)
    spacing = models.CharField(max_length=255, default='', null=True, blank=True)
    crop_stage = models.CharField(max_length=500, choices=STAGES, blank=True, null=True)
    cultivation = models.BooleanField(null=True, blank=True)
    land_prepration = models.CharField(max_length=500, choices=LAND_PREPARATION, default='', null=True, blank=True)
    inter_crops = models.CharField(max_length=500, choices=CROPS, null=True, blank=True)
    crop_yield = models.CharField(max_length=500, null=True, blank=True)
    planting_date = models.DateField(null=True, blank=True)
    pests = models.CharField(max_length=500, null=True, blank=True, choices=PESTS)
    diseases = models.CharField(max_length=500, null=True, blank=True, choices=DISEASES)
    planting_method = models.CharField(max_length=500, null=True, blank=True, choices=PLANTING_METHOD)
    
    # Weather information
    temperature = models.CharField(max_length=500, default='')
    humidity = models.CharField(max_length=500, default='')
    weather = models.CharField(max_length=500, default='')
    cloud = models.CharField(max_length=500, default='')
    wind_condition = models.CharField(max_length=500, default='')
    atmospheric_pressure = models.CharField(max_length=500, default='')
    location = models.CharField(max_length=500, default='')
    created_at = models.DateTimeField(auto_now_add=True, null=True, blank=True)

    def __str__(self):
        return self.user_name

    class Meta:
        verbose_name = 'CropIntel: Get User Enquiries'
        verbose_name_plural = 'CropIntel: Get User Enquiries'

#FieldIntel Page: Feedback Form
class Feedback(models.Model):
    name = models.CharField(max_length=500)
    mobile_no = models.CharField(max_length=10)
    address = models.TextField()
    date = models.DateField(null=True, blank=True)
    
    class Meta:
        verbose_name = 'User Feedback for W2AI Services'
        verbose_name_plural = 'User Feedback for W2AI Services'

    def __str__(self):
        return self.name
    
    class Meta:
        verbose_name = 'FieldIntel: Get User Feedback for Way2AgriIntel AI Services'
        verbose_name_plural = 'FieldIntel: Get User Feedback for Way2AgriIntel AI Services'

#Service Feedabck and Rating: Inline with Feedback
class ServiceFeedback(models.Model):
    RATING_CHOICES = [
        (5, '★★★★★'),
        (4, '★★★★'),
        (3, '★★★'),
        (2, '★★'),
        (1, '★'), 
    ]
    SERVICES = (('CropIntel','CropIntel'),
                ('AgMachineX','AgMachineX'),
                ('Agri FBI','Agri FBI'),
                ('AgriClinic','AgriClinic'),
                ('NutriTracker','NutriTracker'))
    feedback_user = models.ForeignKey(Feedback, on_delete=models.CASCADE)
    services_used = models.CharField(max_length=255, choices=SERVICES, default='', null=True, blank=True)
    feedback = models.TextField(null=True, blank=True)
    suggestions = models.TextField(default='', null=True, blank=True)
    rating = models.IntegerField(choices=RATING_CHOICES, default=0, null=True, blank=True)
    is_important = models.BooleanField(default=False)

    class Meta:
        verbose_name = 'FieldIntel: Get User Feedback for Way2AgriIntel AI Services'
        verbose_name_plural = 'FieldIntel: Get User Feedback for Way2AgriIntel AI Services'

#FieldIntel: Farm Management Solution Requiremnet Form
class AddedServices(models.Model):
    name = models.CharField(max_length=500)
    mobile_no = models.CharField(max_length=10)
    address = models.TextField()
    farm_size = models.IntegerField()
    crop_details = models.TextField()
    current_farm_tech = models.TextField()
    challenges = models.TextField()
    service_requirement = models.TextField()

    class Meta:
        verbose_name = 'FieldIntel: Get User Farm Management Solutions Requirements Enquiries'
        verbose_name_plural = 'FieldIntel: Get User Farm Management Solutions Requirements Enquiries'
		
#AgriClinic Stored Data: Store the Crop-specific Blanket NPK Values
class Crop(models.Model):
	name = models.CharField(max_length=155)
	blanket_n_value = models.FloatField()
	blanket_p_value = models.FloatField()
	blanket_k_value = models.FloatField()
	stage_one_n_value = models.FloatField()
	stage_one_p_value = models.FloatField()
	stage_one_k_value = models.FloatField()
	stage_two_n_value = models.FloatField()
	stage_two_p_value = models.FloatField()
	stage_two_k_value = models.FloatField()
	stage_three_n_value = models.FloatField()
	stage_three_p_value = models.FloatField()
	stage_three_k_value = models.FloatField()

	def __str__(self):
		return self.name

	class Meta:
		verbose_name = 'AgriClinic: Store Crop-Specific Blanket NPK Values'
		verbose_name_plural = 'AgriClinic: Store Crop-Specific Blanket NPK Values'

from django.core.validators import MaxValueValidator, MinValueValidator
from django.contrib.auth.models import User

# AgriClinic User Enquiry from the AgriClinic User Form
class Advisor(models.Model):
    CROPS = (
        ('Arecanut', 'Arecanut'),
        ('Banana', 'Banana'),
        ('Coconut', 'Coconut'),
        ('Coffee', 'Coffee'),
        ('Cotton', 'Cotton'),
        ('Maize', 'Maize'),
        ('Onion', 'Onion'),
        ('Paddy', 'Paddy'),
        ('Papaya', 'Papaya'),
        ('Pepper', 'Pepper'),
        ('Pomegranate', 'Pomegranate'),
        ('Sugarcane', 'Sugarcane'),
        ('Tomato', 'Tomato'),
        ('Tur', 'Tur'),
        ('Potato', 'Potato'),
        ('Groundnut', 'Groundnut'),
        ('Chili', 'Chili'),
        ('Mango', 'Mango'),
        ('Rose', 'Rose'),
        ('Sapota', 'Sapota'),
        ('Ginger', 'Ginger'),
        ('Citrus (related fruits)', 'Citrus (related fruits)'),
        ('Chrysanthemum', 'Chrysanthemum'),
        ('Grapes', 'Grapes'),
        ('Cauliflower (Cole Crops)', 'Cauliflower (Cole Crops)'),
        ('Carrot', 'Carrot'),
        ('Turmeric', 'Turmeric'),
    )

    CHOICES = (
        ('0.3', 'Low (30%)'),
        ('0.4', 'Medium (40%)'),
        ('0.5', 'High (50%)'),
        ('0.6', 'Very High (60%)'),
    )

    STAGES = (
        ('Early Stage', 'Early Stage'),
        ('Growth Stage', 'Growth Stage'),
        ('Yield Stage', 'Yield Stage'),
    )

    user = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True)  # Optional user reference
    full_name = models.CharField(max_length=255, null=True, blank=True)  # For anonymous users
    whatsapp_no = models.CharField(max_length=10, null=True, blank=True)
    email = models.EmailField(max_length=255, null=True, blank=True)

    crop = models.CharField(choices=CROPS, max_length=255, null=True, default=None)
    crop_area = models.IntegerField(default=1)

    ph_value = models.DecimalField(
        max_digits=3,
        decimal_places=1,
        validators=[MaxValueValidator(14), MinValueValidator(0)],
        null=True,
        blank=True
    )
    n_value = models.FloatField(null=True, blank=True)
    p_value = models.FloatField(null=True, blank=True)
    k_value = models.FloatField(null=True, blank=True)

    crop_stage = models.CharField(choices=STAGES, max_length=255, null=True, default=None)

    village = models.CharField(max_length=255, null=True, blank=True)
    taluk = models.CharField(max_length=500, null=True, blank=True)
    district = models.CharField(max_length=500, null=True, blank=True)
    state = models.CharField(max_length=255, null=True, blank=True)
    zip_code = models.CharField(max_length=255, null=True, blank=True)
    land_area = models.CharField(max_length=100, null=True, blank=True)
    zone = models.CharField(max_length=255, null=True, blank=True)

    class Meta:
        verbose_name = 'AgriClinic: User Enquiry from Nutrient Deficiency Form'
        verbose_name_plural = 'AgriClinic: User Enquiry from Nutrient Deficiency Form'

    def __str__(self):
        return self.full_name if self.full_name else "Anonymous User"

#AgriClinic: Image Recognition Enquiries
class DiseaseRecognition(models.Model):
	CROPS = (('Arecanut','Arecanut'),
             ('Banana','Banana'),
             ('Coconut','Coconut'),
             ('Coffee','Coffee'),
             ('Cotton', 'Cotton'),
             ('Maize','Maize'),
             ('Onion','Onion'),
             ('Paddy','Paddy'),
             ('Papaya','Papaya'),
             ('Pepper','Pepper'),
             ('Pomegranate','Pomegranate'),
             ('Sugarcane','Sugarcane'),
             ('Tomato','Tomato'),
             ('Tur','Tur'),
             ('Potato','Potato'),
             ('Groundnut','Groundnut'),
             ('chili','chili'),
             ('Mango','Mango'),
             ('Rose','Rose'),
             ('Sapota','Sapota'),
             ('Ginger','Ginger'),
             ('Citrus (related fruits)','Citrus (related fruits)'),
             ('Chrysanthemum','Chrysanthemum'),
             ('Grapes','Grapes'),
             ('Cauliflower (Cole Crops)','Cauliflower (Cole Crops)'),
             ('Carrot','Carrot'),
             ('Turmeric','Turmeric'))
	name = models.CharField(max_length=500)
	email = models.EmailField(max_length=500, null=True, blank=True)
	phone = models.CharField(max_length=10)
	state = models.CharField(max_length=500)
	city = models.CharField(max_length=255, null=True, blank=True)
	district = models.CharField(max_length=255, null=True, blank=True)
	taluk = models.CharField(max_length=255, null=True, blank=True)
	crop = models.CharField(max_length=255, choices=CROPS)
	disease_image = CloudinaryField()
	disease_image1=CloudinaryField(null=True,blank=True)
	disease_image2=CloudinaryField(null=True,blank=True)
	disease_image3=CloudinaryField(null=True,blank=True)
	disease_image4=CloudinaryField(null=True,blank=True)
	predicted_class0 = models.CharField(max_length=255, null=True, blank=True)
	predicted_class1 = models.CharField(max_length=255, null=True, blank=True)
	predicted_class2 = models.CharField(max_length=255, null=True, blank=True)
	predicted_class3 = models.CharField(max_length=255, null=True, blank=True)
	predicted_class4 = models.CharField(max_length=255, null=True, blank=True)
	finalpredicted_class = models.CharField(max_length=255, null=True, blank=True)

	class Meta:
		verbose_name = 'AgriClinic: Get User Image Recognition Enquiries'
		verbose_name_plural = 'AgriClinic: Get User Image Recognition Enquiries'

#AgriClinic: Store AgriClinic Products NPK Values
class ACProductNPK(models.Model):
	CATEGORIES = (('Organic Fertilizer','Organic Fertilizer'),
                  ('Inorganic Fertilizer','Inorganic Fertilizer'))
	SUB_CATEGORIES = (('Nano Inforganic Fertilizer','Nano Inforganic Fertilizer'),
                      ('Water Soluble Inorganic Fertilizer','Water Soluble Inorganic Fertilizer'),
                      ('Complex Inorganic Fertilizer','Complex Inorganic Fertilizer'),
                      ('Bulk Organic Fertilizer','Bulk Organic Fertilizer'))
	CROPS = (('Arecanut','Arecanut'),
             ('Banana','Banana'),
             ('Coconut','Coconut'),
             ('Coffee','Coffee'),
             ('Cotton', 'Cotton'),
             ('Maize','Maize'),
             ('Onion','Onion'),
             ('Paddy','Paddy'),
             ('Papaya','Papaya'),
             ('Pepper','Pepper'),
             ('Pomegranate','Pomegranate'),
             ('Sugarcane','Sugarcane'),
             ('Tomato','Tomato'),
             ('Tur','Tur'),
             ('Potato','Potato'),
             ('Groundnut','Groundnut'),
             ('chili','chili'),
             ('Mango','Mango'),
             ('Rose','Rose'),
             ('Sapota','Sapota'),
             ('Ginger','Ginger'),
             ('Citrus (related fruits)','Citrus (related fruits)'),
             ('Chrysanthemum','Chrysanthemum'),
             ('Grapes','Grapes'),
             ('Cauliflower (Cole Crops)','Cauliflower (Cole Crops)'),
             ('Carrot','Carrot'),
             ('Turmeric','Turmeric'))
	crop = models.CharField(max_length=500, null=True, blank=True, choices=CROPS)
	category = models.CharField(max_length=500, choices=CATEGORIES)
	sub_categories = models.CharField(max_length=500, choices=SUB_CATEGORIES)
	product_name = models.CharField(max_length=500)
	quantity_product = models.FloatField(default='')
	product_link = models.CharField(max_length=1000, default='')
	product_image = CloudinaryField(null=True, blank=True)
	nitrogen = models.FloatField(null=True, blank=True, default=0.0)
	phosphorus = models.FloatField(null=True, blank=True, default=0.0)
	potassium = models.FloatField(null=True, blank=True, default=0.0)
	sulphur = models.FloatField(null=True, blank=True,default=0.0)
	calcium = models.FloatField(null=True, blank=True, default=0.0)
	boron = models.FloatField(null=True, blank=True,default=0.0)
	magnesium = models.FloatField(null=True, blank=True,default=0.0)
	zinc = models.FloatField(null=True, blank=True,default=0.0)

	class Meta:
		verbose_name = 'AgriClinic: Store AgriClinic Products NPK Values'
		verbose_name_plural = 'AgriClinic: Store AgriClinic Products NPK Values'

#AgriClinic: Symptom Recognition Knowledge
class SymptomRecognitionKnowledge(models.Model):
	CROPS = (('Arecanut','Arecanut'),
             ('Banana','Banana'),
             ('Coconut','Coconut'),
             ('Coffee','Coffee'),
             ('Cotton', 'Cotton'),
             ('Maize','Maize'),
             ('Onion','Onion'),
             ('Paddy','Paddy'),
             ('Papaya','Papaya'),
             ('Pepper','Pepper'),
             ('Pomegranate','Pomegranate'),
             ('Sugarcane','Sugarcane'),
             ('Tomato','Tomato'),
             ('Tur','Tur'),
             ('Potato','Potato'),
             ('Groundnut','Groundnut'),
             ('chili','chili'),
             ('Mango','Mango'),
             ('Rose','Rose'),
             ('Sapota','Sapota'),
             ('Ginger','Ginger'),
             ('Citrus (related fruits)','Citrus (related fruits)'),
             ('Chrysanthemum','Chrysanthemum'),
             ('Grapes','Grapes'),
             ('Cauliflower (Cole Crops)','Cauliflower (Cole Crops)'),
             ('Carrot','Carrot'),
             ('Turmeric','Turmeric'))
	crop = models.CharField(max_length=255,choices=CROPS)
	disease = models.CharField(max_length=500, null=True, blank=True)
	deficiencies = models.CharField(max_length=500, null=True, blank=True)
	pests = models.CharField(max_length=500, null=True, blank=True)
	symptoms = models.TextField()
	keywords = models.TextField()

	def get_keyword_list(self):
		return self.keywords.split(',')

	def __str__(self):
		return ', '.join(self.get_keyword_list())

	class Meta:
		verbose_name = 'AgriClinic: Store Crop-Ailments Specific Symptoms'	
		verbose_name_plural = 'AgriClinic: Store Crop-Ailments Specific Symptoms'

#AgriClinic: User Symptom Recognition Enquiries
class SymptomsRecognitionInput(models.Model):
	CROPS = (('Arecanut','Arecanut'),
             ('Banana','Banana'),
             ('Coconut','Coconut'),
             ('Coffee','Coffee'),
             ('Cotton', 'Cotton'),
             ('Maize','Maize'),
             ('Onion','Onion'),
             ('Paddy','Paddy'),
             ('Papaya','Papaya'),
             ('Pepper','Pepper'),
             ('Pomegranate','Pomegranate'),
             ('Sugarcane','Sugarcane'),
             ('Tomato','Tomato'),
             ('Tur','Tur'),
             ('Potato','Potato'),
             ('Groundnut','Groundnut'),
             ('chili','chili'),
             ('Mango','Mango'),
             ('Rose','Rose'),
             ('Sapota','Sapota'),
             ('Ginger','Ginger'),
             ('Citrus (related fruits)','Citrus (related fruits)'),
             ('Chrysanthemum','Chrysanthemum'),
             ('Grapes','Grapes'),
             ('Cauliflower (Cole Crops)','Cauliflower (Cole Crops)'),
             ('Carrot','Carrot'),
             ('Turmeric','Turmeric'))
	name = models.CharField(max_length=500, default='')
	whatsapp_no = models.CharField(max_length=10, default='')
	email = models.EmailField(null=True, blank=True)
	state = models.CharField(max_length=500, default='')
	district = models.CharField(max_length=500, null=True, blank=True)
	taluk = models.CharField(max_length=500, null=True, blank=True)
	city = models.CharField(max_length=500, null=True, blank=True)
	crop = models.CharField(max_length=255,choices=CROPS)
	from .models import SymptomRecognitionKnowledge
	keyword_list = []
	for instance in SymptomRecognitionKnowledge.objects.all():
		keyword_list.extend(instance.get_keyword_list())
	KEYWORD_CHOICES = [(keyword, keyword) for keyword in keyword_list]
	keywords = models.CharField(max_length=255)

	class Meta:
		verbose_name = 'AgriClinic: Get User Symptom Recognition Enquiries'
		verbose_name_plural = 'AgriClinic: Get User Symptom Recognition Enquiries'
		


class NutriTracker(models.Model):
    CROP_CHOICES = [
        ("", "-- Select a Crop --"),
        ("Amla", "Amla"),
        ("Areca New", "Areca New"),
        ("Avocado", "Avocado"),
        ("Arecanut", "Arecanut"),
        ("Banana", "Banana"),
        ("Betelvine", "Betelvine"),
        ("Carrot", "Carrot"),
        ("Cashewnut", "Cashewnut"),
        ("Cauliflower (Cole Crops)", "Cauliflower (Cole Crops)"),
        ("Chilli", "Chilli"),
        ("Chrysanthemum", "Chrysanthemum"),
        ("Citrus", "Citrus"),
        ("Cocoa", "Cocoa"),
        ("Coconut", "Coconut"),
        ("Coffee", "Coffee"),
        ("Cotton", "Cotton"),
        ("Curry Leaves", "Curry Leaves"),
        ("Custard Apple", "Custard Apple"),
        ("Dragon Fruit", "Dragon Fruit"),
        ("Drumstick", "Drumstick"),
        ("Durian", "Durian"),
        ("Fig", "Fig"),
        ("Ginger", "Ginger"),
        ("Grapes", "Grapes"),
        ("Groundnut", "Groundnut"),
        ("Guava", "Guava"),
        ("Jack Fruit", "Jack Fruit"),
        ("Jasmin", "Jasmin"),
        ("Kokum", "Kokum"),
        ("Lime", "Lime"),
        ("Macadamia", "Macadamia"),
        ("Mahogani", "Mahogani"),
        ("Maize", "Maize"),
        ("Mango", "Mango"),
        ("Mangosteen", "Mangosteen"),
        ("Mosambi", "Mosambi"),
        ("Nutmeg", "Nutmeg"),
        ("Onion", "Onion"),
        ("Paddy", "Paddy"),
        ("Papaya", "Papaya"),
        ("Pepper", "Pepper"),
        ("Pineapple", "Pineapple"),
        ("Pomegranate", "Pomegranate"),
        ("Potato", "Potato"),
        ("Rambutan", "Rambutan"),
        ("Rose", "Rose"),
        ("Rosewood", "Rosewood"),
        ("Sapota", "Sapota"),
        ("Sugarcane", "Sugarcane"),
        ("Tender Coconut", "Tender Coconut"),
        ("Tomato", "Tomato"),
        ("Tur", "Tur"),
        ("Turmeric", "Turmeric"),
    ]

    MONTH_CHOICES = [(month, month) for month in [
        "January", "February", "March", "April", "May", "June",
        "July", "August", "September", "October", "November", "December"
    ]]

    SOIL_CONDITION_CHOICES = [
        ("", "-- Select Soil Condition --"),
        ("Soft", "Soft"),
        ("Hard", "Hard"),
        ("With Stone", "With Stone"),
    ]

    SOIL_HEALTH_CHOICES = [
        ("", "-- Select Soil Health --"),
        ("Good", "Good"),
        ("Average", "Average"),
        ("Poor", "Poor"),
    ]

    WATER_SOURCE_CHOICES = [
        ("", "-- Select Water Source --"),
        ("Rain Fed", "Rain Fed"),
        ("Borewell", "Borewell"),
        ("Others", "Others"),
    ]

    WATER_AVAILABILITY_CHOICES = [
        ("", "-- Select Water Availability --"),
        ("Very Good Water Availability", "Very Good Water Availability"),
        ("Good Water Availability", "Good Water Availability"),
        ("Average Water Availability", "Average Water Availability"),
        ("Limited Water Availability", "Limited Water Availability"),
        ("Poor Water Availability", "Poor Water Availability"),
    ]

    NUTRIENT_CHOICES = [
        ("", "-- Select Nutrient --"),
        ("Organic Matter", "Organic Matter"),
        ("Nitrogen (N)", "Nitrogen (N)"),
        ("Phosphorus (P)", "Phosphorus (P)"),
        ("Potassium (K)", "Potassium (K)"),
        ("Calcium (Ca)", "Calcium (Ca)"),
        ("Magnesium (Mg)", "Magnesium (Mg)"),
        ("Sulphur (S)", "Sulphur (S)"),
        ("Iron (Fe)", "Iron (Fe)"),
        ("Manganese (Mn)", "Manganese (Mn)"),
        ("Zinc (Zn)", "Zinc (Zn)"),
        ("Copper (Cu)", "Copper (Cu)"),
        ("Boron (B)", "Boron (B)"),
        ("Molybdenum (Mo)", "Molybdenum (Mo)"),
    ]

    IRRIGATION_METHOD_CHOICES = [
        ("", "-- Select Irrigation Method --"),
        ("Drip", "Drip"),
        ("Flood", "Flood"),
        ("Sprinkler", "Sprinkler"),
        ("Others", "Others"),
    ]

    CROP_STAGE_CHOICES = [
        ("", "-- Select Crop Stage --"),
        ("Early Stage", "Early Stage"),
        ("Vegetative Stage", "Vegetative Stage"),
        ("Yielding Stage", "Yielding Stage"),
    ]

    FERTILIZER_TYPE_CHOICES = [
        ("", "-- Select Fertilizer Type --"),
        ("Organic Fertilizer", "Organic Fertilizer"),
        ("Inorganic Fertilizer", "Inorganic Fertilizer"),
        ("FYM", "FYM"),
    ]

    # Farmer Information
    name = models.CharField(max_length=100, null=True, blank=True)
    whatsapp_number = models.CharField(max_length=15, null=True, blank=True)
    district = models.CharField(max_length=100, null=True, blank=True)
    taluk = models.CharField(max_length=100, null=True, blank=True)
    address = models.TextField(null=True, blank=True)
    extent_of_land = models.FloatField(null=True, blank=True)

    # Plot Information
    plot_name = models.CharField(max_length=100, null=True, blank=True)
    crop_grown = models.CharField(max_length=100, choices=CROP_CHOICES, null=True, blank=True)
    land_area = models.FloatField(null=True, blank=True)
    crop_density = models.IntegerField(null=True, blank=True)

    # Soil Information
    soil_condition = models.CharField(max_length=100, choices=SOIL_CONDITION_CHOICES, null=True, blank=True)
    soil_health = models.CharField(max_length=100, choices=SOIL_HEALTH_CHOICES, null=True, blank=True)
    soil_ph = models.FloatField(null=True, blank=True)
    water_source = models.CharField(max_length=100, choices=WATER_SOURCE_CHOICES, null=True, blank=True)
    water_availability = models.CharField(max_length=100, choices=WATER_AVAILABILITY_CHOICES, null=True, blank=True)
	
    soil_rich_nutrients = models.TextField(max_length=100, choices=NUTRIENT_CHOICES, null=True, blank=True)
    soil_avg_nutrients = models.TextField(max_length=100, choices=NUTRIENT_CHOICES, null=True, blank=True)
    soil_poor_nutrients = models.TextField(max_length=100, choices=NUTRIENT_CHOICES, null=True, blank=True)

    # Cultivation Information
    sowing_month = models.CharField(max_length=50, choices=MONTH_CHOICES, null=True, blank=True)
    harvesting_month = models.CharField(max_length=50, choices=MONTH_CHOICES, null=True, blank=True)
    irrigation_method = models.CharField(max_length=100, choices=IRRIGATION_METHOD_CHOICES, null=True, blank=True)
    nutrient_application_times = models.IntegerField(null=True, blank=True)
	
    # Soil Test Report Values
    nitrogen_value = models.FloatField(null=True, blank=True)
    potassium_value = models.FloatField(null=True, blank=True)
    phosphorous_value = models.FloatField(null=True, blank=True)
    secondary_nutrients_value = models.FloatField(null=True, blank=True)
    micronutrients_value = models.FloatField(null=True, blank=True)
    organic_carbon_value = models.FloatField(null=True, blank=True)

    # Fertilizer Purchase Details
    crop_fertilizer_applied = models.CharField(max_length=100, choices=CROP_CHOICES, null=True, blank=True)
    crop_stage = models.CharField(max_length=100, choices=CROP_STAGE_CHOICES, null=True, blank=True)
    fertilizer_name = models.CharField(max_length=100, null=True, blank=True)
    nutrient_deficiency = models.CharField(max_length=100, choices=NUTRIENT_CHOICES, null=True, blank=True)
    fertilizer_type = models.CharField(max_length=100, choices=FERTILIZER_TYPE_CHOICES, null=True, blank=True)
    manufacturer_name = models.CharField(max_length=100, null=True, blank=True)
    fertilizer_quantity = models.FloatField(null=True, blank=True)
    fertilizer_purchase_date = models.DateField(null=True, blank=True)

    def __str__(self):
        return f"{self.name or 'Unknown'} - {self.plot_name or 'Unknown'} - {self.crop_grown or 'Unknown'}"

    class Meta:
        verbose_name = "NutriTracker Form"
        verbose_name_plural = "NutriTracker Forms"


class FBI(models.Model):
    # Your Information
    name = models.CharField(max_length=100, null=True, blank=True)
    whatsapp_number = models.CharField(max_length=10, null=True, blank=True)
    district = models.CharField(max_length=100, null=True, blank=True)
    taluk = models.CharField(max_length=100, null=True, blank=True)
    address = models.TextField(max_length=200, null=True, blank=True)
    land_extent = models.FloatField(max_length=20, null=True, blank=True)

    # Agri FBI Info
    USER_CHOICES = [
        ('Seller', 'Seller (Farmer)'),
        ('Buyer', 'Buyer'),
    ]
    user_type = models.CharField(max_length=10, choices=USER_CHOICES, null=True, blank=True)

    def __str__(self):
        return f"{self.name} - {self.user_type}"

    class Meta:
        verbose_name = "Agri FBI Form"
        verbose_name_plural = "Agri FBI Forms"


class CropDetail(models.Model):
    fbi = models.ForeignKey(FBI, on_delete=models.CASCADE, related_name='crop_details')
    
    CROP_CHOICES = [
        ('Paddy', 'Paddy'),
        ('Wheat', 'Wheat'),
        ('Maize', 'Maize'),
        ('Sugarcane', 'Sugarcane'),
        ('Cotton', 'Cotton'),
        ('Groundnut', 'Groundnut'),
        ('Tomato', 'Tomato'),
        ('Potato', 'Potato'),
        ('Onion', 'Onion'),
        ('Chilli', 'Chilli'),
    ]
    
    crop_name = models.CharField(max_length=50, choices=CROP_CHOICES)
    crop_quantity = models.FloatField(help_text="Quantity in Quintal")
    crop_variety = models.CharField(max_length=100)

    def __str__(self):
        return f"{self.fbi.name} - {self.crop_name} ({self.crop_quantity} quintals)"
