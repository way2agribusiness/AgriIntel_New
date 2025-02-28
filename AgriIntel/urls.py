"""
URL configuration for AgriIntel project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path,include
from django.conf import settings
from django.conf.urls.static import static
from django.contrib.sitemaps import views 
from W2AI.sitemap import HomePageSitemap, AboutUsPageSitemap, ContactUsPageSitemap, AgMachineXPageSitemap, CropIntelPageSitemap
from W2AI.sitemap import AgriClinicPageSitemap, FBIPageSitemap, NutriTrackerPageSitemap, FieldIntelPageSitemap,FieldIntelFeedbackPageSitemap
from W2AI.sitemap import AddedServicesPageSitemap,RegisterPageSitemap
from W2AI.sitemap import LoginPageSitemap
import os
from django.http import HttpResponse
from django.views import View

admin.site.site_header = 'Way2AgriIntel Admin'
admin.site.index_title = 'Admin'
sitemaps = {
    'home': HomePageSitemap,
    'aboutus': AboutUsPageSitemap,
    'contactus': ContactUsPageSitemap,
	'cropintel':CropIntelPageSitemap,
	'agriclinic':AgriClinicPageSitemap,
	'agmachinex': AgMachineXPageSitemap,
	'fbi':FBIPageSitemap,
	'nutritracker':NutriTrackerPageSitemap,
	'field-intel':FieldIntelPageSitemap,
	'feedback':FieldIntelFeedbackPageSitemap,
	'farm-management-solutions':AddedServicesPageSitemap,
	'register':RegisterPageSitemap,
	'login':LoginPageSitemap,
}

class RobotsTxtView(View):
    def get(self, request):
        file_path = os.path.join(settings.BASE_DIR, 'robots.txt')

        try:
            with open(file_path, 'r') as file:
                content = file.read()
        except FileNotFoundError:
            content = ""

        return HttpResponse(content, content_type='text/plain')

urlpatterns = [
    path('admin/master-console-npcs6/', admin.site.urls),
    path('', include('W2AI.urls')),
	path('sitemap.xml', views.sitemap, {'sitemaps': sitemaps}, name='django.contrib.sitemaps.views.sitemap'),
	path('robots.txt', RobotsTxtView.as_view(), name='robots.txt'),

] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
