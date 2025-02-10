from django.contrib.sitemaps import Sitemap
import datetime
from django.urls import reverse
from .models import ATSContactInfo
from django.utils.text import slugify

class HomePageSitemap(Sitemap):
    changefreq = 'daily'
    priority = 1.0

    def items(self):
        return ['home']  

    def location(self, item):
        return reverse('W2AI:home')
    
    def lastmod(self,obj):
        return datetime.datetime.today()
    
class AboutUsPageSitemap(Sitemap):
    changefreq = 'weekly'
    priority = 1.0

    def items(self):
        return ['aboutus']

    def location(self, item):
        return reverse('W2AI:aboutus')
    
    def lastmod(self,obj):
        return datetime.datetime.today()
    

class ContactUsPageSitemap(Sitemap):
    changefreq = 'monthly'
    priority = 0.7
    

    def items(self):
        return ['contactus']

    def location(self, item):
        return reverse('W2AI:contactus') 
    
    def lastmod(self,obj):
        return datetime.datetime.today()

class CropIntelPageSitemap(Sitemap):
    changefreq = 'weekly'
    priority = 1.0
    

    def items(self):
        return ['cropintel']

    def location(self, item):
        return reverse('W2AI:cropintel')
    
    def lastmod(self,obj):
        return datetime.datetime.today()

class AgriClinicPageSitemap(Sitemap):
    changefreq = 'daily'
    priority = 1.0
    

    def items(self):
        return ['agriclinic']

    def location(self, item):
        return reverse('W2AI:agriclinic') 
    
    def lastmod(self,obj):
        return datetime.datetime.today()

class AgMachineXPageSitemap(Sitemap):
    changefreq = 'daily'
    priority = 1.0
    

    def items(self):
        return ['agmachinex']

    def location(self, item):
        return reverse('W2AI:agmachinex') 
    
    def lastmod(self,obj):
        return datetime.datetime.today()

class NutriTrackerPageSitemap(Sitemap):
    changefreq = 'daily'
    priority = 1.0
    

    def items(self):
        return ['nutritracker']

    def location(self, item):
        return reverse('W2AI:nutritracker') 
    
    def lastmod(self,obj):
        return datetime.datetime.today()

class FBIPageSitemap(Sitemap):
    changefreq = 'daily'
    priority = 1.0
    

    def items(self):
        return ['fbi']

    def location(self, item):
        return reverse('W2AI:agri-fbi') 
    
    def lastmod(self,obj):
        return datetime.datetime.today()

class FieldIntelPageSitemap(Sitemap):
    changefreq = 'daily'
    priority = 1.0
    

    def items(self):
        return ['field-intel']

    def location(self, item):
        return reverse('W2AI:field-intel') 
    
    def lastmod(self,obj):
        return datetime.datetime.today()

class FieldIntelFeedbackPageSitemap(Sitemap):
    changefreq = 'daily'
    priority = 1.0
    

    def items(self):
        return ['feedback']

    def location(self, item):
        return reverse('W2AI:feedback') 
    
    def lastmod(self,obj):
        return datetime.datetime.today()

class AddedServicesPageSitemap(Sitemap):
    changefreq = 'daily'
    priority = 1.0
    

    def items(self):
        return ['farm-management-solutions']

    def location(self, item):
        return reverse('W2AI:custom-service') 
    
    def lastmod(self,obj):
        return datetime.datetime.today()

class AgritechMartPageSitemap(Sitemap):
    changefreq = 'daily'
    priority = 1.0
    

    def items(self):
        return ['agritech-mart']

    def location(self, item):
        return reverse('W2AI:ats') 
    
    def lastmod(self,obj):
        return datetime.datetime.today()

class AgritechMartCountryCategoryPageSitemap(Sitemap):
	changefreq = 'daily'
	priority = 1.0

	def items(self):
		return ATSContactInfo.objects.all()

	def location(self, obj):
		return reverse('W2AI:ats-category-company', args=[obj.category.category_slug, slugify(obj.contact_company_name)]) 

	def lastmod(self,obj):
		return datetime.date.today()

class RegisterPageSitemap(Sitemap):
    changefreq = 'daily'
    priority = 1.0
    

    def items(self):
        return ['register']

    def location(self, item):
        return reverse('W2AI:register_url') 
    
    def lastmod(self,obj):
        return datetime.datetime.today()

class LoginPageSitemap(Sitemap):
    changefreq = 'daily'
    priority = 1.0
    

    def items(self):
        return ['login']

    def location(self, item):
        return reverse('W2AI:login_url') 
    
    def lastmod(self,obj):
        return datetime.datetime.today()
