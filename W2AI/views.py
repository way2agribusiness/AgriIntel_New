from django.shortcuts import render, redirect
from rest_framework.views import APIView
from rest_framework.response import Response
from django.http import HttpResponseRedirect
from rest_framework import status
from .forms import CustomUserCreationForm, FBIForm, PlotFormSet, LoginForm, CustomPasswordChangeForm, AdvisorForm,  ContactForm
from .forms import  get_feedback_formset
from .forms import AgMachineXUserInputForm, UserProfileForm, CropIntelUserInputForm, FeedbackForm, AddedServiceForm
from .forms import FundRequirementForm, ActualSalesForm, QtyRequirementForm, DiseaseRecognitionForm, SymptomRecognitionForm, AgMachinexFilterForm
from .models import SeoContent, ContactNumber,UserProfile, Plot,Brands, Credentials, Contact, Advisor, Crop
from .models import NutriTracker, AgMachineSpecifications, AgMachineXUserInput,FBI, AgriFBI, FBIEnquiry, CurrentMonthReport
from .models import LastMonthReport, SeasonalReport, CropIntelInput, Feedback, AddedServices
from .models import CropIntelKnowledge, FundRequirement, MarketPlannerStrategy, QtyRequirement, DiseaseRecognition, SymptomsRecognitionInput
from .models import SymptomRecognitionKnowledge, ACProductNPK,  Highlights
from .models import ServiceFeedback,IntroTextDescription
from django.http import HttpResponse
from django.contrib.auth import login, authenticate, logout
from django.urls import reverse
from django.contrib.auth.decorators import login_required
from django.contrib.auth import update_session_auth_hash
from itertools import groupby
from django.core.exceptions import ObjectDoesNotExist
from django.shortcuts import get_object_or_404
import requests
import json
import csv
import datetime
import pytz
import os
from django.conf import settings
from .notifications import send_notification
from .serializers import FeedbackSerializer, AddedServicesSerializer, ContactSerializer, AgMachineXUserInputSerializer, AgMachineSpecificationsSerializer, CropIntelKnowledgeSerializer, FBISerializer
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework.viewsets import ModelViewSet
from rest_framework.exceptions import NotFound
import pandas as pd
import numpy as np
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
from io import BytesIO
import base64
from scipy import stats
from .ml_utils import load_pretrained_model
# from keras.losses import SparseCategoricalCrossentropy
# import tensorflow as tf
# from keras.optimizers import SGD
# from keras.preprocessing.image import load_img, img_to_array
# from keras.preprocessing import image_dataset_from_directory
import requests
from datetime import datetime, timedelta, date, timezone
from django.http import JsonResponse
from rest_framework import viewsets
import phonenumbers
import socket
from ip2geotools.databases.noncommercial import DbIpCity
from geopy.geocoders import Nominatim
from django import forms
from django.db.models import Count, Avg

#----------------------- Below are the fucntion to fetch the IP, Location ------------------------------
def getIP(request):
	x_forwarded_for = request.META.get('HTTP_X_FORWARDED_FOR')
	if x_forwarded_for:
		ip = x_forwarded_for.split(',')[0]
	else:
		ip = request.META.get('REMOTE_ADDR')
	return ip

def get_ip_location(ip_address):
	api_key = '5976d2ca492e4abc88c7091a0f55f09a'
	api_url = 'https://ipgeolocation.abstractapi.com/v1/?api_key=5976d2ca492e4abc88c7091a0f55f09a&ip_address=103.148.39.22'
	response = requests.get(api_url)
	return response.content

def get_location(request):
	if request.method == 'POST':
		data = json.loads(request.body)
		latitude = data.get('latitude')
		longitude = data.get('longitude')
		city = data.get('city')
		country = data.get('country')
		region = data.get('region')
		postal_code = data.get('postal_code')
		request.session['latitude'] = latitude
		request.session['longitude'] = longitude
		request.session['city'] = city
		request.session['country'] = country
		request.session['region'] = region
		request.session['postal_code'] = postal_code
		return JsonResponse({'success': True})
	return JsonResponse({'success': False})

#----------------------- Above are the fucntions to fetch the IP, Location ------------------------------

#----------------------- Below are the fucntions for SEO and  Success From ------------------------------
@login_required
def form_submission_success_message_view(request):
	return render(request,'form-success-message.html')

def BacklinksView(request):
	links_list = SeoContent.objects.values_list('backlinks', flat=True)
	links_list = [links.split(',') for links in links_list if links]
	unique_links = [list(set(sublist)) for sublist in links_list]
	return render(request, 'external_link.html',{'links_list':unique_links})

#----------------------- Above are the fucntions for SEO and  Success From ------------------------------

#------------------------------------ Below is Home Page View -------------------------------------------
def HomeView(request):
	title=''
	desc=''
	seo = SeoContent.objects.all()
	highlight = Highlights.objects.all()
	feedbacks = ServiceFeedback.objects.all()
	desc=IntroTextDescription.objects.all()
	for i in seo:
		if i.page == 'home':
			title = i.meta_title
			desc = i.meta_description
	url = request.build_absolute_uri(request.path)
	total_reviews = ServiceFeedback.objects.count()
	avg_rating_query = ServiceFeedback.objects.aggregate(avg_rating=Avg('rating'))
	if avg_rating_query['avg_rating'] is not None:
		avg_rating = round(avg_rating_query['avg_rating'], 1)
	else:
		avg_rating=0.0
	percentage5 = int((ServiceFeedback.objects.filter(rating=5).count()/total_reviews)*100 if total_reviews >0 else 0)
	percentage4 = int((ServiceFeedback.objects.filter(rating=4).count()/total_reviews)*100 if total_reviews >0 else 0)
	percentage3 = int((ServiceFeedback.objects.filter(rating=3).count()/total_reviews)*100 if total_reviews >0 else 0)
	percentage2 = int((ServiceFeedback.objects.filter(rating=2).count()/total_reviews)*100 if total_reviews >0 else 0)
	percentage1 = int((ServiceFeedback.objects.filter(rating=1).count()/total_reviews)*100 if total_reviews >0 else 0)
	if request.method == 'POST':
		data=request.POST.get('number')
		if data:
			try:
				val_num=phonenumbers.parse(data,'IN')
				if not phonenumbers.is_valid_number(val_num) or str(val_num.national_number)[0] not in ['9','8','7','6']:
					return HttpResponseRedirect(request.path)
				else:
					city =request.session.get('city')
					region=request.session.get('region')
					number=ContactNumber()
					number.phone_number=data
					number.city=city
					number.region=region
					number.Time=timezone.now()
					number.save()
					return HttpResponseRedirect(request.path)
			except:
				return HttpResponseRedirect(request.path)

	return render(request,'home.html', {'title':title,'desc':desc,'canonical':url, 'highlight':highlight,
									 'feedbacks':feedbacks,'avg_rating':avg_rating,'total_review':total_reviews,'per5':percentage5,'per4':percentage4,'per3':percentage3,'per2':percentage2,'per1':percentage1})

#------------------------------------ Above is Home Page View -------------------------------------------

#------------------------------------- Below is About Us View -------------------------------------------
def AboutView(request):
	title=''
	desc=''
	seo = SeoContent.objects.all()
	for i in seo:
		if i.page == 'home':
			title = i.meta_title
			desc = i.meta_description
	url = request.build_absolute_uri(request.path)
	brands = Brands.objects.all()
	c_images = Credentials.objects.order_by('type_of_image')
	grouped_images = []
	for key, group in groupby(c_images, key=lambda x: x.get_type_of_image_display()):
		grouped_images.append({'type_of_image': key, 'images': list(group)})
	return render(request,'aboutus.html',{'brands':brands,'grouped_images':grouped_images,'title':title,'desc':desc,'canonical':url})

#------------------------------------- Above is About Us View -------------------------------------------

#------------------------------------- Below is Feedback Form View in Field Intel -------------------------------------------

def feedback_view(request):
	url = request.build_absolute_uri(request.path)
	feedback_form = FeedbackForm()
	services_count = len(ServiceFeedback.SERVICES)
	formset = get_feedback_formset(extra_forms=services_count)
	feedback_formset = formset()
	if request.method=='POST':
		feedback_form = FeedbackForm(data=request.POST)
		feedback_formset = formset(data=request.POST, instance=Feedback())
		if feedback_form.is_valid() and feedback_formset.is_valid():
			main_instance=feedback_form.save()
			feedback_formset.instance=main_instance
			feedback_formset.save()
			subject = f'{url}: Service Feedback'
			message = f'''Service Feedback from <em style="color:darkblue">{url}</em>.<br>
            	<strong>Customer Name:</strong> {main_instance.name}<br>
            	<strong>Phone Number: </strong>{main_instance.mobile_no}<br>
            	<strong>Address: </strong>{main_instance.address}'''
			recipient_list = ['dr.prasannad@way2agribusiness.com']
			send_notification(subject, message, recipient_list)
			return redirect(reverse('W2AI:feedback-success'))
		else:
			return render(request, '7. fieldintel/feedback-form.html', {'feedback_form': feedback_form,'feedback_formset':feedback_formset})
	return render(request, '7. fieldintel/feedback-form.html',{'feedback_form':feedback_form,'feedback_formset':feedback_formset})

class FeedbackViewSet(ModelViewSet):
	queryset = Feedback.objects.all()
	serializer_class = FeedbackSerializer

	def create(self,request,*args,**kwargs):
		feedback_form = FeedbackForm(request.POST)
		if feedback_form.is_valid():
			feedback_form.save()
			return redirect(reverse('W2AI:feedback-success'))
		else:
			return Response({'error':feedback_form.errors}, status=400)
		
	def get_feedback_details(self, request):
		feedback_form = FeedbackForm()
		return render(request, '7. fieldintel/feedback-form.html', {'feedback_form': feedback_form})
	
#------------------------------------- Above is Feedback Form View in Field Intel -------------------------------------------

#------------------------------------- Below is Farm Management Solution Form  -------------------------------------------
def added_service_view(request):
	url = request.build_absolute_uri(request.path)
	service_form = AddedServiceForm()
	if request.method=='POST':
		service_form = AddedServiceForm(data=request.POST)
		if service_form.is_valid():
			main_instance=service_form.save()
			subject = f'{url}: Farm Management Solutions'
			message = f'''Farm Management Solutions Response from <em style="color:darkblue">{url}</em>.<br>
            	<strong>Customer Name:</strong> {main_instance.name}<br>
            	<strong>Phone Number: </strong>{main_instance.mobile_no}<br>
            	<strong>Address: </strong>{main_instance.address}'''
			recipient_list = ['dr.prasannad@way2agribusiness.com']
			send_notification(subject, message, recipient_list)
			return redirect(reverse('W2AI:feedback-success'))
		else:
			return render(request, '7. fieldintel/custservices.html', {'service_form': service_form})
	return render(request, '7. fieldintel/custservices.html',{'service_form':service_form})

class addedServiceViewSet(ModelViewSet):
	queryset = AddedServices.objects.all()
	serializer_class = AddedServicesSerializer

	def create(self,request,*args,**kwargs):
		service_form = AddedServiceForm(request.POST)
		if service_form.is_valid():
			service_form.save()
			return redirect(reverse('W2AI:feedback-success'))
		else:
			return Response({'error':service_form.errors}, status=400)
		
	def get_feedback_details(self, request):
		service_form = AddedServiceForm()
		return render(request, '7. fieldintel/custservices.html', {'service_form': service_form})

def feedback_success_view(request):
	return render(request,'7. fieldintel/feedback_thank_you.html')

#------------------------------------- Above is Farm Management Solution Form  -------------------------------------------

#----------------------- Below is Contact and message form in main page ------------------------------
def contact(request):
	url = request.build_absolute_uri(request.path)
	highlight = Highlights.objects.all()
	seo = SeoContent.objects.filter(page="contactus").first()
	title=seo.meta_title if seo else ''
	desc=seo.meta_description if seo else ''
	key=seo.keywords if seo else ''
	if request.method == "POST":
		form = ContactForm(data=request.POST)
		if form.is_valid():
			number = form.cleaned_data['phone']
			try:
				parsed_number = phonenumbers.parse(number,'IN')
				if not phonenumbers.is_valid_number(parsed_number) and str(parsed_number.national_number)[0] not in ['9', '8', '7', '6']:
					message = 'Invalid Phone number: Must be of 10 digit length and Must start with 9, 8, 7 or 6'
					form = ContactForm(data=request.POST)
					return render(request, 'contact.html',{'canonical':url,'logo':logo,'title':title,'desc':desc,'key':key,'message':message,'form':form, 'message':message})
				elif str(parsed_number.national_number)[0] not in ['9', '8', '7', '6']:
					message = 'Invalid Phone Number: Must start with 9, 8, 7, or 6'
					form = ContactForm(data=request.POST)
					return render(request, 'contact.html',{'canonical':url,'logo':logo,'title':title,'desc':desc,'key':key,'form':form,'message':message})
				elif not phonenumbers.is_valid_number(parsed_number):
					message = 'Invalid Phone Number: must be of 10 digit'
					form = ContactForm(data=request.POST)
					return render(request, 'contact.html',{'canonical':url,'logo':logo,'title':title,'desc':desc,'key':key,'form':form,'message':message})
			except phonenumbers.phonenumberutil.NumberParseException:
				message = 'Invalid Phone number'
				form = ContactForm(data=request.POST)
				return render(request, 'contact.html',{'canonical':url,'logo':logo,'title':title,'desc':desc,'key':key, 'form':form,'message':message})
			main_instance=form.save()
			instance = Contact.objects.get(id=main_instance.id)
			subject = f'Message from Contact Us of way2agriintel.com'
			message = f'''Message from <strong>Contact Us </strong> of <em>way2agriintel.com</em><br>
            			<strong>Customer Name: </strong>{instance.name}<br>
                        <strong>Phone Number: </strong>{instance.phone}<br>
                        <strong>Customer Message/Enquiry: </strong>{instance.comments}'''
			recipient_list = ['dr.prasannad@way2agribusiness.com']
			send_notification(subject, message, recipient_list)
			redirected_path=reverse('W2AI:contactack')
			return redirect(redirected_path)
	else:
		form = ContactForm()
	return render(request, 'contact.html',{'canonical':url,'title':title,'desc':desc,'key':key,'form':form})

class contactusViewSet(ModelViewSet):
	queryset = Contact.objects.all()
	serializer_class = ContactSerializer
#----------------------- Above is Contact and message form in main page ------------------------------

#----------------------- Below is Contact number entering in footer ------------------------------
from django.shortcuts import render, redirect
from django.contrib import messages
from django.core.validators import RegexValidator
from .models import ContactNumber

def handle_contact_form(request):
    if request.method == 'POST':
        phone_number = request.POST.get('number')

        # Validate phone number (exactly 10 digits)
        if phone_number and len(phone_number) == 10 and phone_number.isdigit():
            # Get user IP
            ip_address = getIP(request)  

            # Fetch location data
            location_data = get_ip_location(ip_address)
            location_data = json.loads(location_data)  # Convert to JSON

            # Extract city and region
            city = location_data.get('city', '')  
            region = location_data.get('region', '')

            # Save to database
            ContactNumber.objects.create(
                phone_number=phone_number,
                city=city,
                region=region
            )

            messages.success(request, f"Thank you! We will contact you soon. Location: {city}, {region}")
        else:
            messages.error(request, "Please enter a valid 10-digit phone number.")

        return redirect(request.META.get('HTTP_REFERER', '/'))

    return redirect('/')
#----------------------- Contact number entering in footer above ------------------------------

def thankyou(request):
	return render(request,'contactus_thankyou.html')

def get_agromonitoring_weather(weather_api_id, lat, lon, units):
    base_url = "https://api.openweathermap.org/data/2.5/weather"
    params = {
        'lon':lon,
		'lat':lat,
		'units':units,
        'appid': weather_api_id,
    }
    response = requests.get(url=base_url, params=params)
    weather_data = response.json()
    return weather_data

def get_weather_info_history(loc, start_date):
	api_key = '4d2ad9f72eb64b1c9e560941241403'
	api = f"https://www.weatherapi.com/history/q/{loc}-1107187?loc=1107187"
	api_call = f"https://api.weatherapi.com/v1/history.json?key={api_key}&q={loc}&dt={start_date}"
	response = requests.get(api_call)
	full_weather_data = response.json()
	return full_weather_data

def get_weather_info_future(api_key, loc, date):
	api_call = f"https://api.weatherapi.com/v1/future.json?key={api_key}&q={loc}&dt={date}"
	print(api_call)
	response=requests.get(api_call)
	full_weather_data = response.json()
	return full_weather_data

#Authentication Views
def register_view(request):
	url = request.build_absolute_uri(request.path)
	if request.method == "POST":
		form = CustomUserCreationForm(data=request.POST)
		if form.is_valid():
			form.save()
			return redirect(reverse('W2AI:login_url'))
	else:
		form = CustomUserCreationForm()
	return render(request,'1. authentication/register.html',{'form':form, 'canonical':url})

def login_view(request):
	url = request.build_absolute_uri(request.path)
	if request.method == 'POST':
		form = LoginForm(data=request.POST)
		if form.is_valid():
			username = form.cleaned_data['username']
			password = form.cleaned_data['password']
			user = authenticate(request, username=username, password=password)
			if user is not None:
				login(request, user)
				url = reverse('W2AI:dashboard')
				return redirect(url)
	else:
		form = LoginForm()
	return render(request, '1. authentication/login.html', {'form': form,'canonical':url})

@login_required
def logout_view(request):
	logout(request)
	url = reverse('W2AI:login_url')
	return redirect(url)

@login_required
def dashboardView(request):
    user_data = UserProfile.objects.filter(user=request.user).first()
    
    if not user_data:
        return render(request, '1. authentication/dashboard.html', 
                      {'error': 'User profile not found. Please create a profile.'})

    latitude = request.session.get('latitude')
    longitude = request.session.get('longitude')
    city = request.session.get('city')
    country = request.session.get('country')
    region = request.session.get('region')
    postal_code = request.session.get('postal_code')

    if not all([latitude, longitude, city, country, region, postal_code]):
        return render(request, '1. authentication/dashboard.html', 
                      {'error': 'Location not provided'})

    weather_api_key = '6249320d11d4bc13fe46a32d29695afb'
    units = 'metric'
    weather_data = get_agromonitoring_weather(weather_api_key, latitude, longitude, units)

    # Extract weather data safely
    description = weather_data.get('weather', [{}])[0].get('description', 'N/A')
    icon = weather_data.get('weather', [{}])[0].get('icon', 'N/A')
    main = weather_data.get('weather', [{}])[0].get('main', 'N/A')
    temp = weather_data.get('main', {}).get('temp', 0)
    humid = weather_data.get('main', {}).get('humidity', 0)
    feels_like = weather_data.get('main', {}).get('feels_like', 0)
    wind_deg = weather_data.get('wind', {}).get('deg', 0)
    wind = weather_data.get('wind', {}).get('speed', 0)
    cloud = weather_data.get('clouds', {}).get('all', 0)

    # Fetch weather data from CSV
    csv_url = "https://res.cloudinary.com/dm71xhdxd/raw/upload/v1724061927/Static%20Images/FinalAlldistricts_wlqjel.csv"
    response = requests.get(csv_url)
    content = response.content.decode('utf-8').splitlines()
    csv_reader = csv.DictReader(content)

    for row in csv_reader:
        if row['district'] == city:
            temp = row.get('tempavg', temp)
            humid = row.get('humidityavg', humid)
            pressure = row.get('sealevelpressureavg', 'N/A')
            wind = row.get('windspeedavg', wind)
            cloud = row.get('cloudcoveravg', cloud)

    # Convert sunrise and sunset times safely
    sunrise = weather_data.get('sys', {}).get('sunrise')
    sunset = weather_data.get('sys', {}).get('sunset')

    sunrise_time_chennai = sunset_time_chennai = "N/A"
    if sunrise and sunset:
        sunrise_datetime_utc = datetime.fromtimestamp(sunrise, tz=timezone.utc)  # ✅ FIXED
        sunset_datetime_utc = datetime.fromtimestamp(sunset, tz=timezone.utc)  # ✅ FIXED
        chennai_timezone = pytz.timezone('Asia/Kolkata')

        sunrise_time_chennai = sunrise_datetime_utc.astimezone(chennai_timezone).strftime('%I:%M %p')
        sunset_time_chennai = sunset_datetime_utc.astimezone(chennai_timezone).strftime('%I:%M %p')

    # Update user profile data
    user_data.state = region
    if user_data.state != 'Karnataka':
        user_data.city = city
    else:
        user_data.district = city
    user_data.save()

    plots = Plot.objects.filter(user_profile=user_data).first()

    context = {
        'country': country,
        'region': region,
        'city': city,
        'postal_code': postal_code,
        'longitude': longitude,
        'latitude': latitude,
        'description': description,
        'icon': icon,
        'temp': temp,
        'humid': humid,
        'wind_deg': wind_deg,
        'wind': wind,
        'cloud': cloud,
        'sunrise': sunrise_time_chennai,
        'sunset': sunset_time_chennai,
        'day': date.today(),
        'main': main,
        'feels_like': feels_like,
        'pressure': pressure,
        'user_data': user_data,
        'plots': plots,
    }

    return render(request, '1. authentication/dashboard.html', context)

@login_required
def changePasswordView(request):
    if request.method == 'POST':
        form = CustomPasswordChangeForm(request.user, data=request.POST)
        if form.is_valid():
            user = form.save()
            update_session_auth_hash(request, user)
            return redirect(reverse('W2AI:password_change_done'))  # Fixed URL name
    else:
        form = CustomPasswordChangeForm(request.user)
    
    return render(request, '1. authentication/change_password.html', {'form': form})

@login_required
def password_change_done(request):
    return render(request, '1. authentication/password_change_done.html')

def load_json_data(file_path):
	with open(file_path, 'r') as json_file:
		data=json.load(json_file)
	return data


@login_required
def user_profile_view(request):
    json_file_path = os.path.join(settings.BASE_DIR, 'W2AI/static/data.json')
    data = load_json_data(json_file_path)
    user_data = UserProfile.objects.get(user=request.user)
    districts = data[0]['districts']
    
    if request.method == 'POST':
        form = UserProfileForm(data=request.POST, instance=request.user.profile if hasattr(request.user, 'profile') else None)
        plot_formset = PlotFormSet(data=request.POST, instance=request.user.profile)
        city = request.session.get('city')  # This will give the district value and not city value
        region = request.session.get('region')
        zip_code = request.session.get('postal_code')

        if not city or not region or not zip_code:
            return render(request, '1. authentication/dashboard.html', {'error': 'Location not provided'})

        if form.is_valid() and plot_formset.is_valid():
            selected_village = form.cleaned_data['village']
            selected_village = selected_village[0].upper()+selected_village[1:]
            selected_taluk = form.cleaned_data['taluk']
            selected_zone_district = form.cleaned_data['zone_district']
            zone_list = {
                        'Plain-North Zone':['Bidar', 'Gulbarga(Kalaburgi)', 'Bijapur(Vijayapura)', 'Yadgir', 'Belgaum', 'Bagalkot', 'Raichur', 'Dharwad', 'Gadag', 'Koppala', 'Haveri','Bellary'],
                        'Plain-South Zone':['Chamarajanagar', 'Mysuru', 'Mandya', 'Hassan', 'Ramanagara', 'Bengaluru Rural', 'Kolar', 'Chikkaballapur', 'Tumkur', 'Chikmagalur(East)', 'Chitradurga', 'Davanagere', 'Anantapur', 'Chittoor(Andhra Pradesh)', 'Krishangiri(Tamil Nadu)'],
                        'Coastal Zone':['Dakshina Kannada(Mangalore)','Udupi','Uttara Kannada(West)','Kasargod(Kerala)'],
                        'Western (Malenadu) Zone':['Uttara Kannada(East)','Shimoga','Chikmagalur(West)','Coorg(Madikeri)(Kodagu)','Wayanad(Kerala)','Nilgiris(Tamil Nadu)']
                    }    
            selected_zone = [zone for zone, location in zone_list.items() if selected_zone_district in location]

            replaced_zone = str(selected_zone).replace(']','').replace('[','').replace("'",'')
            filtered_data = {}
            for district in districts:
                for subdistrict in district['subDistricts']:
                    if subdistrict['subDistrict'] == selected_taluk:
                        filtered_data[subdistrict['subDistrict']] = subdistrict['villages']
            if selected_village not in filtered_data[selected_taluk]:
                message = "Enter Accurate Village name for the selected Taluk"
                return render(request, '1. authentication/complete_profile.html',{'form':form,'plot_formset': plot_formset, 'message':message})

            else:
                user_profile, created = UserProfile.objects.update_or_create(
                    user=request.user,
                    defaults={
                        'taluk': selected_taluk,
                        'village':selected_village,
                        'district':city,
                        'state':region,
                        'zip_code':zip_code,
                        'zone_district':selected_zone_district,
                        'zone':replaced_zone
                    }
                )

                plot_formset.instance = user_profile
                plot_formset.save()
                return redirect(reverse('W2AI:dashboard'))
    else:
        form = UserProfileForm()
        plot_formset = PlotFormSet()
    return render(request, '1. authentication/complete_profile.html',{'form':form,'plot_formset': plot_formset, 'user_data': user_data})

@login_required
def delete_plot(request, plot_id):
    if request.method == 'POST':  # Change to check for POST method
        plot = get_object_or_404(Plot, id=plot_id, user_profile__user=request.user)
        plot.delete()
        return JsonResponse({'status': 'success'})
    return JsonResponse({'status': 'error'}, status=405)


#------------------------------- Below is Crop Intel Form Views --------------------------------------------------

#CropIntel Views
def CropIntelView(request):
	title=''
	desc=''
	seo = SeoContent.objects.all()
	for i in seo:
		if i.page == 'home':
			title = i.meta_title
			desc = i.meta_description
	url = request.build_absolute_uri(request.path)
	plot_data = [plot.user_profile.user.username for plot in Plot.objects.all()]
	return render(request,'2. cropintel/cropintel.html',{'title':title,'desc':desc,'canonical':url,'plot_data':plot_data})


import logging
logger = logging.getLogger(__name__)

# @login_required
# def crop_intel_feeding_form(request):
#     user_profile = get_object_or_404(UserProfile, user=request.user)
#     plots = Plot.objects.filter(user_profile=user_profile)
    
#     # Initialize weather variables with default values
#     weather_data = {
#         'temp': None,
#         'humid': None,
#         'pressure': None,
#         'wind': None,
#         'wind_deg': None,
#         'cloud': None,
#         'description': None
#     }
    
#     # Get location data from session
#     location_data = {
#         'latitude': request.session.get('latitude'),
#         'longitude': request.session.get('longitude'),
#         'city': request.session.get('city'),
#         'country': request.session.get('country'),
#         'region': request.session.get('region'),
#         'postal_code': request.session.get('postal_code')
#     }
    
#     # Get weather data
#     weather_api_key = '44efc615f164e272266fd2cb3bd2ad3a'
#     units = 'metric'
#     api_weather_data = get_agromonitoring_weather(
#         weather_api_key, 
#         location_data['latitude'], 
#         location_data['longitude'], 
#         units
#     )
    
#     # Get district data
#     csv_url = "https://res.cloudinary.com/dm71xhdxd/raw/upload/v1724061927/Static%20Images/FinalAlldistricts_wlqjel.csv"
#     try:
#         response = requests.get(csv_url)
#         response.raise_for_status()  # Raise an exception for bad status codes
#         content = response.content.decode('utf-8').splitlines()
#         csv_reader = csv.DictReader(content)
        
#         user_zone_district = user_profile.zone_district
        
#         # Find matching district and update weather data
#         for row in csv_reader:
#             if row['district'] == user_zone_district:
#                 weather_data.update({
#                     'description': api_weather_data['weather'][0]['description'],
#                     'temp': row['tempavg'],
#                     'humid': row['humidityavg'],
#                     'pressure': row['sealevelpressureavg'],
#                     'wind': row['windspeedavg'],
#                     'wind_deg': api_weather_data['wind']['deg'],
#                     'cloud': row['cloudcoveravg']
#                 })
#                 break
        
#         if weather_data['temp'] is None:
#             raise ValueError(f"No matching district found for {user_zone_district}")
            
#     except (requests.RequestException, ValueError) as e:
#         # Log the error and set default values
#         logger.error(f"Error fetching district data: {str(e)}")
#         weather_data.update({
#             'description': 'Data unavailable',
#             'temp': '0',
#             'humid': '0',
#             'pressure': '0',
#             'wind': '0',
#             'wind_deg': '0',
#             'cloud': '0'
#         })

#     # Get options for form fields
#     form_options = {
#         'crop_grown_options': Plot.CROPS,
#         'soil_condition_options': Plot.SOIL_CONDITION,
#         'soil_health_options': Plot.SOIL_HEALTH,
#         'soil_ph_options': Plot.pH,
#         'soil_nutrients_options': Plot.SOIL_NUTRIENTS,
#         'water_source_options': Plot.WATER_SOURCES,
#         'water_avail_options': Plot.WATER_SUFFICIENCIES
#     }

#     if request.method == 'POST':
#         form = CropIntelUserInputForm(data=request.POST)
#         if form.is_valid():
#             user_input_form = form.save(commit=False)
            
#             # Get plot information
#             plot_input = request.POST.get('plot')
#             plot_info = Plot.objects.filter(plot_name=plot_input).first()
            
#             # Update user input form with form data
#             form_data = {
#                 'plot_name': request.POST.get('plot_name'),
#                 'crop_grown': request.POST.get('crop_grown'),
#                 'land_area': request.POST.get('land_area'),
#                 'soil_condition': request.POST.get('soil_condition'),
#                 'soil_health': request.POST.get('soil_health'),
#                 'soil_ph': request.POST.get('soil_ph'),
#                 'soil_rich_nutrients': request.POST.get('soil_rich_nutrients'),
#                 'soil_average_nutrients': request.POST.get('soil_avg_nutrients'),
#                 'soil_poor_nutrients': request.POST.get('soil_poor_nutrients'),
#                 'water_source': request.POST.get('water_source'),
#                 'water_availability': request.POST.get('water_avail')
#             }
            
#             # Update user input form and plot info
#             for field, value in form_data.items():
#                 setattr(user_input_form, field, value)
#                 if plot_info:
#                     setattr(plot_info, field, value)
            
#             # Set user details
#             user_input_form.user_name = user_profile.name
#             user_input_form.phone_no = user_profile.whatsapp_no
            
#             # Set weather data
#             user_input_form.temperature = weather_data['temp']
#             user_input_form.humidity = weather_data['humid']
#             user_input_form.weather = weather_data['description']
#             user_input_form.atmospheric_pressure = weather_data['pressure']
#             user_input_form.cloud = weather_data['cloud']
#             user_input_form.wind_condition = f"{weather_data['wind']} and direction {weather_data['wind_deg']}"
#             user_input_form.location = user_profile.zone_district
            
#             # Save the form
#             user_input_form.save()
            
#             # Get the saved instance
#             instance = CropIntelInput.objects.get(id=user_input_form.id)
            
#             # Prepare notification
#             subject = 'Crop Intel Service Enquiry'
#             message = f'''Enquiry is <br>
#                         <strong>Customer Name: </strong> {instance.user_name}<br>
#                         <strong>Customer Phone Number: </strong> {instance.phone_no}<br>'''
            
#             return redirect(reverse('W2AI:form-message'))
#     else:
#         form = CropIntelUserInputForm()

#     context = {
#         'form': form,
#         'user_profile': user_profile,
#         'plots': plots,
#         **form_options
#     }
    
#     return render(request, '2. cropintel/cropintel_form.html', context)
from .forms import CropIntelUserInputForm

logger = logging.getLogger(__name__)

def crop_intel_feeding_form(request):
    user = request.user
    user_profile = None
    plots = None

    if user.is_authenticated:
        user_profile = get_object_or_404(UserProfile, user=user)
        plots = Plot.objects.filter(user_profile=user_profile)

    # Default weather data
    weather_data = {
        'temp': None,
        'humid': None,
        'pressure': None,
        'wind': None,
        'wind_deg': None,
        'cloud': None,
        'description': None
    }

    # Get location data from session
    location_data = {
        'latitude': request.session.get('latitude'),
        'longitude': request.session.get('longitude'),
        'city': request.session.get('city'),
        'country': request.session.get('country'),
        'region': request.session.get('region'),
        'postal_code': request.session.get('postal_code')
    }

    # Get weather data
    weather_api_key = '44efc615f164e272266fd2cb3bd2ad3a'
    units = 'metric'
    api_weather_data = None
    
    if location_data['latitude'] and location_data['longitude']:
        try:
            api_weather_data = get_agromonitoring_weather(
                weather_api_key, 
                location_data['latitude'], 
                location_data['longitude'], 
                units
            )
        except Exception as e:
            logger.error(f"Error fetching weather data: {str(e)}")

    # Get district data
    csv_url = "https://res.cloudinary.com/dm71xhdxd/raw/upload/v1724061927/Static%20Images/FinalAlldistricts_wlqjel.csv"
    try:
        response = requests.get(csv_url)
        response.raise_for_status()
        content = response.content.decode('utf-8').splitlines()
        csv_reader = csv.DictReader(content)

        user_zone_district = user_profile.zone_district if user.is_authenticated and user_profile else None

        for row in csv_reader:
            if row['district'] == user_zone_district:
                weather_data.update({
                    'description': api_weather_data['weather'][0]['description'] if api_weather_data else 'Data unavailable',
                    'temp': row['tempavg'],
                    'humid': row['humidityavg'],
                    'pressure': row['sealevelpressureavg'],
                    'wind': row['windspeedavg'],
                    'wind_deg': api_weather_data['wind']['deg'] if api_weather_data else '0',
                    'cloud': row['cloudcoveravg']
                })
                break

        if weather_data['temp'] is None:
            weather_data.update({
                'description': 'Data unavailable',
                'temp': '0',
                'humid': '0',
                'pressure': '0',
                'wind': '0',
                'wind_deg': '0',
                'cloud': '0'
            })

    except (requests.RequestException, ValueError) as e:
        logger.error(f"Error fetching district data: {str(e)}")
        weather_data.update({
            'description': 'Data unavailable',
            'temp': '0',
            'humid': '0',
            'pressure': '0',
            'wind': '0',
            'wind_deg': '0',
            'cloud': '0'
        })

    # Get options for form fields from Plot model
    form_options = {
        'crop_grown_options': Plot.CROPS,
        'soil_condition_options': Plot.SOIL_CONDITION,
        'soil_health_options': Plot.SOIL_HEALTH,
        'soil_ph_options': Plot.pH,
        'soil_nutrients_options': Plot.SOIL_NUTRIENTS,
        'water_source_options': Plot.WATER_SOURCES,
        'water_avail_options': Plot.WATER_SUFFICIENCIES
    }

    if request.method == 'POST':
        form = CropIntelUserInputForm(data=request.POST)
        if form.is_valid():
            user_input_form = form.save(commit=False)

            # Get plot information if user is authenticated
            if user.is_authenticated:
                plot_input = request.POST.get('selected_plot')
                plot_info = Plot.objects.filter(plot_name=plot_input, user_profile=user_profile).first()
            else:
                plot_info = None

            # Update user input form with form data
            form_data = {
                'plot_name': request.POST.get('plot_name'),
                'crop_grown': request.POST.get('crop_grown'),
                'land_area': request.POST.get('land_area'),
                'soil_condition': request.POST.get('soil_condition'),
                'soil_health': request.POST.get('soil_health'),
                'soil_ph': request.POST.get('soil_ph'),
                'soil_rich_nutrients': request.POST.get('soil_rich_nutrients'),
                'soil_average_nutrients': request.POST.get('soil_avg_nutrients'),
                'soil_poor_nutrients': request.POST.get('soil_poor_nutrients'),
                'water_source': request.POST.get('water_source'),
                'water_availability': request.POST.get('water_avail')
            }

            for field, value in form_data.items():
                setattr(user_input_form, field, value)
                if plot_info:
                    setattr(plot_info, field, value)

            # Handle user details
            if user.is_authenticated:
                user_input_form.user_name = user_profile.name
                user_input_form.phone_no = user_profile.whatsapp_no
                user_input_form.district = user_profile.zone_district
                user_input_form.location = user_profile.zone_district
            else:
                user_input_form.user_name = request.POST.get('user_name')
                user_input_form.phone_no = request.POST.get('phone_no')
                user_input_form.district = request.POST.get('district')
                user_input_form.taluk = request.POST.get('taluk')
                user_input_form.address = request.POST.get('address')
                user_input_form.location = request.POST.get('district')

            # Set weather data
            user_input_form.temperature = weather_data['temp']
            user_input_form.humidity = weather_data['humid']
            user_input_form.weather = weather_data['description']
            user_input_form.atmospheric_pressure = weather_data['pressure']
            user_input_form.cloud = weather_data['cloud']
            user_input_form.wind_condition = f"{weather_data['wind']} and direction {weather_data['wind_deg']}"

            # Save the form
            user_input_form.save()

            # Update plot if needed
            if plot_info:
                plot_info.save()

            return redirect(reverse('W2AI:form-message'))
        else:
            # Handle form errors
            logger.error(f"Form errors: {form.errors}")
    else:
        form = CropIntelUserInputForm()

    context = {
        'form': form,
        'user_profile': user_profile,
        'plots': plots,
        'is_authenticated': user.is_authenticated,
        **form_options
    }

    return render(request, '2. cropintel/cropintel_form.html', context)
#------------------------------- Above is Crop Intel Form Views --------------------------------------------------

@login_required
def crop_intel_recommendation(request):
	user_profile = UserProfile.objects.get(user=request.user)
	user_input = CropIntelInput.objects.filter(user_name=user_profile.name).order_by('-created_at').first()
	if user_input:
		pass
    # Get all knowledge entries
	knowledge = CropIntelKnowledge.objects.all()
    
	user_input_knowledge = []
    # Iterate through knowledge items and pair with the user input
	for i in range(len(knowledge)):
		knowledge_item = knowledge[i]
		user_input_knowledge.append({
            'user_input': user_input,
            'recommendation': knowledge_item,
        } )
    
	return render(request, '2. cropintel/cropintel-recommendation.html', {
        'user_input': user_input,
        'knowledge': knowledge,
        'user_input_knowledge': user_input_knowledge
    })

#AgMachineX Views
def AgMachineXView(request):
	title=''
	desc=''
	seo = SeoContent.objects.all()
	for i in seo:
		if i.page == 'home':
			title = i.meta_title
			desc = i.meta_description
	url = request.build_absolute_uri(request.path)
	return render(request,'3. agmachinex/machinexai.html', {'title':title,'desc':desc,'canonical':url})

# @login_required
# def agmachinex_user_input_view(request):
# 	if request.method == 'POST':
# 		form = AgMachineXUserInputForm(data=request.POST)
# 		if form.is_valid():
# 			user_input_form = form.save(commit=False)
# 			profile = UserProfile.objects.get(user=request.user)
# 			user_input_form.full_name = profile.name
# 			user_input_form.whatsapp_no = profile.whatsapp_no
# 			user_input_form.email_id = request.user.email if request.user.email else None
# 			user_input_form.state = profile.state
# 			user_input_form.district = profile.district if profile.district else None
# 			user_input_form.taluk = profile.taluk if profile.taluk else None
# 			user_input_form.village = profile.village if profile.village else None
# 			user_input_form.zip_code = profile.zip_code if profile.zip_code else None
# 			user_input_form.zone = profile.zone if profile.zone else None
# 			user_input_form.save()
# 			instance = AgMachineXUserInput.objects.get(id=user_input_form.id)
# 			instance_id = instance.id
# 			#url = reverse('W2AI:agmachinex-recommendation', args=[instance_id])
# 			#return redirect(url)
# 			# subject = 'AgMachineX Service Enquiry'
# 			# message = f'''Enquiry is <br>
# 			# 			<strong>Customer Name: </strong> {instance.full_name}<br>
# 			# 			<strong>Customer Phone Number: </strong> {instance.whatsapp_no}<br>'''
# 			# send_notification(subject, message, ['dr.prasannad@way2agribusiness.com'])
# 			return redirect(reverse('W2AI:form-message'))
# 	else:
# 		form = AgMachineXUserInputForm()
# 	return render(request,'3. agmachinex/agmachinex_user_input.html',{'form':form})

from django.contrib.auth.models import AnonymousUser
def agmachinex_user_input_view(request):
    if request.method == 'POST':
        form = AgMachineXUserInputForm(data=request.POST)
        if form.is_valid():
            user_input_form = form.save(commit=False)
            
            # If user is authenticated, auto-fill fields
            if request.user.is_authenticated and not isinstance(request.user, AnonymousUser):
                try:
                    profile = UserProfile.objects.get(user=request.user)
                    
                    user_input_form.full_name = profile.name or form.cleaned_data.get("full_name")
                    user_input_form.whatsapp_no = profile.whatsapp_no or form.cleaned_data.get("whatsapp_no")
                    user_input_form.email_id = request.user.email if request.user.email else form.cleaned_data.get("email_id")
                    user_input_form.state = profile.state or form.cleaned_data.get("state")
                    user_input_form.district = profile.district or form.cleaned_data.get("district")
                    user_input_form.taluk = profile.taluk or form.cleaned_data.get("taluk")
                    user_input_form.village = profile.village or form.cleaned_data.get("village")
                    user_input_form.zip_code = profile.zip_code or form.cleaned_data.get("zip_code")
                    user_input_form.zone = profile.zone or form.cleaned_data.get("zone")
                
                except UserProfile.DoesNotExist:
                    pass  # If no profile, allow manual entry
            
            # Save form (for both registered and anonymous users)
            user_input_form.save()
        return redirect(reverse('W2AI:form-message'))
    else:
        form = AgMachineXUserInputForm()
    return render(request, '3. agmachinex/agmachinex_user_input.html', {'form': form})

class AgMachineXUserInputViewSet(ModelViewSet):
	queryset = AgMachineXUserInput.objects.all()
	serializer_class = AgMachineXUserInputSerializer

	def get_ag_userinput_details(self, request):
		ag_userinput_form = AgMachineXUserInputForm()
		return render(request, 'contact.html', {'ag_userinput_form': ag_userinput_form})

class AgMachineSpecificationsView(ModelViewSet):
	queryset = AgMachineSpecifications.objects.all()
	serializer_class = AgMachineSpecificationsSerializer

# class ExistingUserPurchaseHistoryView(ModelViewSet):
# 	queryset = NutriTracker.objects.all()
# 	serializer_class = ExistingFarmerPurchaseHistorySerializer()

class CropIntelKnowledgeView(ModelViewSet):
	queryset = CropIntelKnowledge.objects.all()
	serializer_class = CropIntelKnowledgeSerializer

class FBIReportsView(ModelViewSet):
	queryset = AgriFBI.objects.all()
	serializer_class = FBISerializer

@login_required
def agmachinex_recommendation_view(request, instance_id):
	profile = UserProfile.objects.get(user=request.user)
	user_datas = AgMachineXUserInput.objects.filter(full_name=profile.name, id=instance_id)
	for user_data in user_datas:
		machine_req = user_data.machinery_req
		land_area =  user_data.land_area
		crop = user_data.crop
		budget =  user_data.budget
	machine_specs = AgMachineSpecifications.objects.filter(product_category=machine_req)
	product = []
	product = [
		machine_spec.product_name
		for machine_spec in machine_specs
			if (land_area == machine_spec.land_extent) and (
				(budget == 'Below than Rs. 10000' and machine_spec.price < 10000) or
				(budget == 'Between Rs. 10000 to Rs. 20000' and 10000 <= machine_spec.price < 20000) or
				(budget == 'Between Rs. 20000 to Rs. 50000' and 20000 <= machine_spec.price < 50000) or
				(budget == 'Between Rs. 50000 to Rs. 1,00,000' and 50000 <= machine_spec.price < 100000) or
				(budget == 'Between Rs. 1,00,000 to Rs. 1,50,000' and 100000 <= machine_spec.price < 150000) or
				(budget == 'Between Rs. 1,50,000 to Rs. 2,00,000' and 150000 <= machine_spec.price < 200000) or
				(budget == 'Between Rs. 2,00,000 to Rs. 2,50,000' and 200000 <= machine_spec.price <= 250000) or
				(budget == 'Above than Rs. 2,50,000' and machine_spec.price > 250000)
			)
	]
	recommend_machine = []
	for i in product:
		try:
			machine = AgMachineSpecifications.objects.get(product_name=i)
			recommend_machine.append(machine)
		except ObjectDoesNotExist:
			print("Machine not found.")
	form = AgMachinexFilterForm(request.POST or None)
	if request.method == 'POST':
		if form.is_valid():
			selected_brand = form.cleaned_data['brand']
			selected_crop = form.cleaned_data['crop']
			filtered_products = {product.product_name:(product.brand,product.product_image.url,product.soil_type,product.price,product.website_link, product.land_extent, product.crop) for product in recommend_machine if selected_brand and product.brand == selected_brand}
			filtered_products_crop = {product.product_name:(product.brand, product.product_image.url, product.soil_type, product.price, product.website_link, product.land_extent, product.crop) for product in recommend_machine if selected_crop and product.crop == selected_crop}
			filtered_all = {product:(details[0],details[1],details[2],details[3],details[4],details[5],details[6])for product, details in filtered_products.items() if selected_brand and selected_crop and details[6] == selected_crop}
			return render(request, '3. agmachinex/agmachines_recommendation.html', {'filtered_products': filtered_products,'filtered_products_crop': filtered_products_crop,'filtered_all': filtered_all, 'enquired_landarea':land_area, 'enquired_crop':crop, 'enquired_budget': budget, 'enquired_machine':machine_req,'form':form,'selected_brand':selected_brand,'selected_crop':selected_crop})
	return render(request, '3. agmachinex/agmachines_recommendation.html',{'recommended_product':recommend_machine, 'enquired_landarea':land_area, 'enquired_crop':crop, 'enquired_budget': budget, 'enquired_machine':machine_req,'form':form})

#---------------------------------------------- Below is AgriFBI views --------------------------------------------
def FBIView(request):
	title=''
	desc=''
	seo = SeoContent.objects.all()
	for i in seo:
		if i.page == 'fbi':
			title = i.meta_title
			desc = i.meta_description
	url = request.build_absolute_uri(request.path)
	plot_data = [plot.user_profile.user.username for plot in Plot.objects.all()]
	return render(request,'4. fbi/fbi.html', {'title':title,'desc':desc,'canonical':url,'plot_data':plot_data})

from django.forms import formset_factory
from .models import FBI, CropDetail
from .forms import FBIForm, CropDetailFormSet
def fbi_form(request):
    if request.method == 'POST':
        fbi_form = FBIForm(request.POST)
        crop_formset = CropDetailFormSet(request.POST, prefix='crops')
        
        if fbi_form.is_valid() and crop_formset.is_valid():
            fbi = fbi_form.save()
            
            for form in crop_formset:
                if form.is_valid() and form.cleaned_data and not form.cleaned_data.get('DELETE', False):
                    crop = form.save(commit=False)
                    crop.fbi = fbi
                    crop.save()
            
            # Add success message or redirect
        return redirect(reverse('W2AI:form-message'))
    else:
        fbi_form = FBIForm()
        crop_formset = CropDetailFormSet(prefix='crops')
    
    return render(request, '4. fbi/fbi_input_crop.html', {
        'fbi_form': fbi_form,
        'crop_formset': crop_formset
    })

# @login_required
# def fbi_crop_selection(request):
# 	crops = AgriFBI.objects.all()
# 	if request.method == 'POST':
# 		enquiry = FBIEnquiry()
# 		profile = UserProfile.objects.get(user=request.user)
# 		enquiry.phone_no = profile.whatsapp_no
# 		enquiry.user_name = profile.name
# 		selected_crops = request.POST.getlist('crops')
# 		enquiry.crop = [selected_crop for selected_crop in selected_crops]
# 		enquiry.save()
# 		instance = FBIEnquiry.objects.get(id=enquiry.id)
# 		instance_id = instance.id
# 		url = reverse('W2AI:fbi-report-generation', args=[instance_id])
# 		#return redirect(url)
# 		subject = 'Agri FBI Service Enquiry'
# 		message = f'''Enquiry is <br>
# 					<strong>Customer Name: </strong> {instance.user_name}<br>
# 					<strong>Customer Phone Number: </strong> {instance.phone_no}<br>'''
# 		send_notification(subject, message, ['dr.prasannad@way2agribusiness.com'])
# 		return redirect(reverse('W2AI:form-message'))
# 	return render(request, '4. fbi/fbi_input_crop.html', {'crops':crops})

@login_required
def fbi_report_generate(request, instance_id):
	profile = FBIEnquiry.objects.get(id=instance_id)
	crop_str = profile.crop
	crops_list = [crop.strip(" '[]") for crop in crop_str.split(',')]
	current_report = CurrentMonthReport.objects.filter(crop__crop__in=crops_list)
	hist_report = LastMonthReport.objects.filter(crop__crop__in=crops_list)
	season_report = SeasonalReport.objects.filter(crop__crop__in = crops_list)
	return render(request,'4. fbi/fbi_generate_report.html',{'profile':profile, 'crops_list':crops_list, 'current_report':current_report, 'hist_report':hist_report, 'season_report':season_report})

@login_required
def fund_requirement(request, user_type):
	if request.method == 'POST':
		form = FundRequirementForm(data=request.POST)
		if form.is_valid():
			fund_form = form.save(commit=False)
			profile = UserProfile.objects.get(user=request.user)
			fund_form.user_type = user_type
			fund_form.name = profile.name
			fund_form.phone_no = profile.whatsapp_no
			fund_form.email = request.user.email if request.user.email else None
			fund_form.state = profile.state
			fund_form.district = profile.district if profile.district else None
			fund_form.taluk = profile.taluk if profile.taluk else None
			fund_form.city = profile.city if profile.city else None
			fund_form.land_area = profile.land_area if profile.land_area else None
			fund_form.save()
			instance = FundRequirement.objects.get(id = fund_form.id)
			instance_crop = instance.id
			url = reverse('W2AI:market-planner-strategies', args=[instance_crop])
			return redirect (url)
	else:
		form = FundRequirementForm()
	return render(request,'4. fbi/market-planner/fund_requirement.html',{'form':form})

@login_required
def qty_requirement(request, user_type):
	if request.method == 'POST':
		form = QtyRequirementForm(data=request.POST)
		if form.is_valid():
			qty_form = form.save(commit=False)
			profile = UserProfile.objects.get(user=request.user)
			qty_form.user_type = user_type
			qty_form.name = profile.name
			qty_form.phone_no = profile.whatsapp_no
			qty_form.email = request.user.email if request.user.email else None
			qty_form.state = profile.state
			qty_form.district = profile.district if profile.district else None
			qty_form.taluk = profile.taluk if profile.taluk else None
			qty_form.city = profile.city if profile.city else None
			qty_form.land_area = profile.land_area if profile.land_area else None
			qty_form.save()
			instance = QtyRequirement.objects.get(id = qty_form.id)
			instance_crop = instance.id
			url = reverse('W2AI:market-planner-strategies', args=[instance_crop])
			return redirect (url)
	else:
		form = QtyRequirementForm()
	return render(request,'4. fbi/market-planner/quantity_requirement.html',{'form':form})

@login_required
def market_planner(request, instance_crop):
	crops = FundRequirement.objects.get(id=instance_crop)
	crop = crops.crops
	price_outlook = MarketPlannerStrategy.objects.get(crops=crop)
	excel_sheet_path = price_outlook.upload_excel.url
	df = pd.read_csv(excel_sheet_path)
	df['Total Revenue'] = df['Price /50Kg'] * ((float(crops.quantity_available))/50)
	df.to_csv(excel_sheet_path, index=False)
	summary_stats = df.groupby('Month')['Price /50Kg'].agg(['mean', 'median', 'std'])
	
	fund_req_jan = crops.amount_jan if crops.amount_jan else None
	fund_req_feb = crops.amount_feb if crops.amount_feb else None
	fund_req_mar = crops.amount_mar if crops.amount_mar else None
	fund_req_apr = crops.amount_apr if crops.amount_apr else None
	fund_req_may = crops.amount_may if crops.amount_may else None
	fund_req_jun = crops.amount_jun if crops.amount_jun else None
	fund_req_jul = crops.amount_jul if crops.amount_jul else None
	fund_req_aug = crops.amount_aug if crops.amount_aug else None
	fund_req_sep = crops.amount_sep if crops.amount_sep else None
	fund_req_oct = crops.amount_oct if crops.amount_oct else None
	fund_req_nov = crops.amount_nov if crops.amount_nov else None
	fund_req_dec = crops.amount_dec if crops.amount_dec else None

	jan_df = df[df['Month'] == '24-Jan']
	feb_df = df[df['Month'] == '24-Feb']
	mar_df = df[df['Month'] == '24-Mar']
	apr_df = df[df['Month'] == '24-Apr']
	may_df = df[df['Month'] == '24-May']
	jun_df = df[df['Month'] == '24-Jun']
	jul_df = df[df['Month'] == '24-Jul']
	aug_df = df[df['Month'] == '24-Aug']
	sep_df = df[df['Month'] == '24-Sep']
	oct_df = df[df['Month'] == '24-Oct']
	nov_df = df[df['Month'] == '24-Nov']
	dec_df = df[df['Month'] == '24-Dec']

	jan_df_revenue = float(jan_df['Total Revenue'].iloc[0])
	feb_df_revenue = float(feb_df['Total Revenue'].iloc[0])
	mar_df_revenue = float(mar_df['Total Revenue'].iloc[0])
	apr_df_revenue = float(apr_df['Total Revenue'].iloc[0])
	may_df_revenue = float(may_df['Total Revenue'].iloc[0])
	jun_df_revenue = float(jun_df['Total Revenue'].iloc[0])
	jul_df_revenue = float(jul_df['Total Revenue'].iloc[0])
	aug_df_revenue = float(aug_df['Total Revenue'].iloc[0])
	sep_df_revenue = float(sep_df['Total Revenue'].iloc[0])
	oct_df_revenue = float(oct_df['Total Revenue'].iloc[0])
	nov_df_revenue = float(nov_df['Total Revenue'].iloc[0])
	dec_df_revenue = float(dec_df['Total Revenue'].iloc[0])
	if crops.user_type=='farmer':
		quantity_available = (float(crops.quantity_available))
		price_per_unit=jan_df_revenue/quantity_available
		quantity_needed = float(fund_req_jan)/price_per_unit if fund_req_jan else None
		fund_obtain = quantity_needed * price_per_unit if quantity_needed else None

		price_per_unit_feb = feb_df_revenue/quantity_available
		quantity_needed_feb = float(fund_req_feb)/price_per_unit_feb if fund_req_feb else None
		fund_obtain_feb = quantity_needed_feb * price_per_unit_feb if quantity_needed_feb else None

		price_per_unit_mar = mar_df_revenue/quantity_available
		quantity_needed_mar = float(fund_req_mar)/price_per_unit_mar if fund_req_mar else None
		fund_obtain_mar = quantity_needed_mar * price_per_unit_mar if quantity_needed_mar else None

		price_per_unit_apr = apr_df_revenue/quantity_available
		quantity_needed_apr = float(fund_req_apr)/price_per_unit_apr if fund_req_apr else None
		fund_obtain_apr = quantity_needed_apr * price_per_unit_apr if quantity_needed_apr else None

		price_per_unit_may = may_df_revenue/quantity_available
		quantity_needed_may = float(fund_req_may)/price_per_unit_may if fund_req_may else None
		fund_obtain_may = quantity_needed_may * price_per_unit_may if quantity_needed_may else None

		price_per_unit_jun = jun_df_revenue/quantity_available
		quantity_needed_jun = float(fund_req_jun)/price_per_unit_jun if fund_req_jun else None
		fund_obtain_jun = quantity_needed_jun * price_per_unit_jun if quantity_needed_jun else None

		price_per_unit_jul = jul_df_revenue/quantity_available
		quantity_needed_jul = float(fund_req_jul)/price_per_unit_jul if fund_req_jul else None
		fund_obtain_jul = quantity_needed_jul * price_per_unit_jul if quantity_needed_jul else None

		price_per_unit_aug = aug_df_revenue/quantity_available
		quantity_needed_aug = float(fund_req_aug)/price_per_unit_aug if fund_req_aug else None
		fund_obtain_aug = quantity_needed_aug * price_per_unit_aug if quantity_needed_aug else None

		price_per_unit_sep = sep_df_revenue/quantity_available
		quantity_needed_sep = float(fund_req_sep)/price_per_unit_sep if fund_req_sep else None
		fund_obtain_sep = quantity_needed_sep * price_per_unit_sep if quantity_needed_sep else None

		price_per_unit_oct = oct_df_revenue/quantity_available
		quantity_needed_oct = float(fund_req_oct)/price_per_unit_oct if fund_req_oct else None
		fund_obtain_oct = quantity_needed_oct * price_per_unit_oct if quantity_needed_oct else None

		price_per_unit_nov = nov_df_revenue/quantity_available
		quantity_needed_nov = float(fund_req_nov)/price_per_unit_nov if fund_req_nov else None
		fund_obtain_nov = quantity_needed_nov * price_per_unit_nov if quantity_needed_nov else None

		price_per_unit_dec = dec_df_revenue/quantity_available
		quantity_needed_dec = float(fund_req_dec)/price_per_unit_dec if fund_req_dec else None
		fund_obtain_dec = quantity_needed_dec * price_per_unit_dec if quantity_needed_dec else None
	
				
	plt.figure(figsize = (10, 3))
	plt.bar(df['Month'], df['Price /50Kg'], color ='darkgoldenrod', width = 0.4)
	plt.plot(df['Month'], df['Price /50Kg'], marker='o', linestyle='-', color='darkgreen')
	plt.xticks( fontsize=10, color='green', fontfamily='Times New Roman')
	plt.yticks(fontsize=10, color='green', fontfamily='Times New Roman')
	plt.xlabel('Month', fontsize=12, fontweight='bold', color='black', labelpad=10, fontfamily='Times New Roman')  # Example styling for xlabel
	plt.ylabel('Price /50Kg', fontsize=12, fontweight='bold', color='black', labelpad=10, fontfamily='Times New Roman')
	plt.title(f'{crop} Price Trends at Major Markets in Karnataka (Year 2024)', fontsize=12, fontweight='bold', color='darkgreen',fontfamily='Times New Roman')
	plt.gca().spines['top'].set_color('lightgray')
	plt.gca().spines['right'].set_color('lightgray')
	plt.gca().spines['left'].set_color('lightgray')
	plt.gca().spines['bottom'].set_color('lightgray')

	plt.gca().spines['top'].set_visible(False)
	plt.gca().spines['right'].set_visible(False)
	plt.gca().spines['left'].set_visible(True)
	plt.gca().spines['bottom'].set_visible(True)

	buffer = BytesIO()
	plt.savefig(buffer, format='webp')
	buffer.seek(0)
	plt.close()
	
	plot_data = base64.b64encode(buffer.getvalue()).decode('utf-8')
	buffer.close()
	return render(request,'4. fbi/market-planner/fund_req_suggestion.html',
			   {'crops':crops,'crop':crop,'price_outlook':price_outlook,'plot_data':plot_data, "df":df, 
	   			"fund_req_jan":float(fund_req_jan) if fund_req_jan else None,'fund_req_feb':float(fund_req_feb) if fund_req_feb else None,
				'fund_req_mar':float(fund_req_mar) if fund_req_mar else None,'fund_req_apr':float(fund_req_apr) if fund_req_apr else None,
				'fund_req_may':float(fund_req_may) if fund_req_may else None,'fund_req_jun':float(fund_req_jun) if fund_req_jun else None,
				'fund_req_jul':float(fund_req_jul) if fund_req_jul else None,'fund_req_aug':float(fund_req_aug) if fund_req_aug else None,
				'fund_req_sep':float(fund_req_sep) if fund_req_sep else None,'fund_req_oct':float(fund_req_oct) if fund_req_oct else None,
				'fund_req_nov':float(fund_req_nov) if fund_req_nov else None,'fund_req_dec':float(fund_req_dec) if fund_req_dec else None,
				'price_per_unit':price_per_unit,'price_per_unit_feb':price_per_unit_feb, 'price_per_unit_mar':price_per_unit_mar,
				'price_per_unit_apr':price_per_unit_apr, 'price_per_unit_may':price_per_unit_may,'price_per_unit_jun':price_per_unit_jun,
				'price_per_unit_jul':price_per_unit_jul, 'price_per_unit_aug':price_per_unit_aug,'price_per_unit_sep':price_per_unit_sep,
				'price_per_unit_oct':price_per_unit_oct,'price_per_unit_nov':price_per_unit_nov,'price_per_unit_dec':price_per_unit_dec,
				'quantity_needed':int(quantity_needed) if quantity_needed else None,'quantity_needed_feb':int(quantity_needed_feb) if quantity_needed_feb else None,
				'quantity_needed_mar':int(quantity_needed_mar) if quantity_needed_mar else None,'quantity_needed_apr':int(quantity_needed_apr) if quantity_needed_apr else None,
				'quantity_needed_may':int(quantity_needed_may) if quantity_needed_may else None,'quantity_needed_jun':int(quantity_needed_jun) if quantity_needed_jun else None,
				'quantity_needed_jul':int(quantity_needed_jul) if quantity_needed_jul else None,'quantity_needed_aug':int(quantity_needed_aug) if quantity_needed_aug else None,
				'quantity_needed_sep':int(quantity_needed_sep) if quantity_needed_sep else None,'quantity_needed_oct':int(quantity_needed_oct) if quantity_needed_oct else None,
				'quantity_needed_nov':int(quantity_needed_nov) if quantity_needed_nov else None,'quantity_needed_dec':int(quantity_needed_dec) if quantity_needed_dec else None,
				'jan_df_revenue':jan_df_revenue,'feb_df_revenue':feb_df_revenue,'mar_df_revenue':mar_df_revenue,
				'apr_df_revenue':apr_df_revenue,'may_df_revenue':may_df_revenue,'jun_df_revenue':jun_df_revenue,
				'jul_df_revenue':jul_df_revenue,'aug_df_revenue':aug_df_revenue,'sep_df_revenue':sep_df_revenue,
				'oct_df_revenue':oct_df_revenue,'nov_df_revenue':nov_df_revenue,'dec_df_revenue':dec_df_revenue,
				'quantity_available':quantity_available, 'fund_obtain':fund_obtain,'fund_obtain_feb':fund_obtain_feb,
				'fund_obtain_mar':fund_obtain_mar,'fund_obtain_apr':fund_obtain_apr,'fund_obtain_may':fund_obtain_may,
				'fund_obtain_jun':fund_obtain_jun,'fund_obtain_jul':fund_obtain_jul,'fund_obtain_aug':fund_obtain_aug,
				'fund_obtain_sep':fund_obtain_sep,'fund_obtain_oct':fund_obtain_oct,'fund_obtain_nov':fund_obtain_nov,
				'fund_obtain_dec':fund_obtain_dec})

@login_required
def actual_sales(request):
	if request.method == 'POST':
		form = ActualSalesForm(data=request.POST)
		if form.is_valid():
			sales_form = form.save(commit=False)
			profile = UserProfile.objects.get(user=request.user)
			sales_form.name = profile.name
			sales_form.phone_no = profile.whatsapp_no
			sales_form.email = request.user.email if request.user.email else None
			sales_form.state = profile.state
			sales_form.district = profile.district if profile.district else None
			sales_form.taluk = profile.taluk if profile.taluk else None
			sales_form.city = profile.city if profile.city else None
			sales_form.land_area = profile.land_area if profile.land_area else None
			sales_form.save()
			url = reverse('W2AI:market-planner-strategies')
			return redirect (url)
	else:
		form =  ActualSalesForm()
	return render(request, '4. fbi/market-planner/actual_sales.html',{'form':form})

#---------------------------------------------- Above is AgriFBI views --------------------------------------------


#-------------------------------------- Below Agri Clinic Related views ------------------------------------------
def AgriClinicView(request):
	title=''
	desc=''
	seo = SeoContent.objects.all()
	for i in seo:
		if i.page == 'home':
			title = i.meta_title
			desc = i.meta_description
	url = request.build_absolute_uri(request.path)
	plot_data = [plot.user_profile.user.username for plot in Plot.objects.all()]
	return render(request,'5. agriclinic/nutriai.html', {'title':title,'desc':desc,'canonical':url,'plot_data':plot_data})

import ssl
ssl._create_default_https_context = ssl._create_unverified_context

from django.contrib.auth import get_user_model
User = get_user_model()

def advisor_view(request):
    if request.method == 'POST':
        form = AdvisorForm(data=request.POST)
        if form.is_valid():
            ac_form = form.save(commit=False)

            if request.user.is_authenticated:
                profile = UserProfile.objects.get(user=request.user)
                ac_form.user = request.user
                ac_form.full_name = profile.name
                ac_form.whatsapp_no = profile.whatsapp_no
                ac_form.email_id = request.user.email if request.user.email else None
            else:
                ac_form.user = None  # Anonymous user

            ac_form.save()

            subject = 'AgriClinic Service Enquiry'
            message = f'''Enquiry is <br>
                        <strong>Customer Name: </strong> {ac_form.full_name}<br>
                        <strong>Customer Phone Number: </strong> {ac_form.whatsapp_no}<br>'''
            
            send_notification(subject, message, ['dr.prasannad@way2agribusiness.com'])

        return redirect(reverse('W2AI:form-message'))
    else:
        form = AdvisorForm()
    
    return render(request, '5. agriclinic/advisorform.html', {'form': form})

@login_required    
def amt_of_nutrient(request,crop_name,id):
	crop=Crop.objects.get(name=crop_name)
	eq_npk = ACProductNPK.objects.all()
	eq_n = {i.product_name: (i.crop,i.nitrogen,i.category,i.sub_categories,i.quantity_product,i.product_image, i.product_link) for i in eq_npk if i.nitrogen is not None}
	eq_p = {i.product_name: (i.crop,i.potassium,i.category,i.sub_categories,i.quantity_product,i.product_image, i.product_link) for i in eq_npk if i.potassium is not None}
	eq_k = {i.product_name: (i.crop,i.phosphorus,i.category,i.sub_categories,i.quantity_product,i.product_image, i.product_link) for i in eq_npk if i.phosphorus is not None}
	n_val=crop.blanket_n_value
	p_val=crop.blanket_p_value
	k_val=crop.blanket_k_value
	
	advisor=Advisor.objects.get(id=id)
	str_true=advisor.available_of_str
	area=advisor.crop_area
	name=advisor.name
	
	if str_true == True:
		amt_nval_added=n_val - advisor.n_value
		amt_pval_added=p_val - advisor.p_value
		amt_kval_added=k_val - advisor.k_value
	else:
		try:
			advisor_nitrogen = float(advisor.nitrogen)
			advisor_phosphorus = float(advisor.phosphorus)
			advisor_potassium = float(advisor.potassium)
		except (ValueError, TypeError):
			messages.error(request, "Invalid nitrogen, phosphorus, or potassium value.")
			return redirect('error_page')
		
		amt_nitrogen_added=n_val * advisor_nitrogen
		amt_phosphorus_added=p_val * advisor_phosphorus
		amt_potassium_added=k_val * advisor_potassium
	stage=advisor.crop_stage
	if str_true == True:
		if stage == 'Early Stage':
			adjusted_nval=(crop.stage_one_n_value/100) * amt_nval_added
			adjusted_pval=(crop.stage_one_p_value/100) * amt_pval_added
			adjusted_kval=(crop.stage_one_k_value/100) * amt_kval_added	
		elif stage == 'Growth Stage':
			adjusted_nval=(crop.stage_two_n_value/100) * amt_nval_added
			adjusted_pval=(crop.stage_two_p_value/100) * amt_pval_added
			adjusted_kval=(crop.stage_two_k_value/100) * amt_kval_added
		else:
			adjusted_nval=(crop.stage_three_n_value/100) * amt_nval_added
			adjusted_pval=(crop.stage_three_p_value/100) * amt_pval_added
			adjusted_kval=(crop.stage_three_k_value/100) * amt_kval_added

		final_nval=adjusted_nval * area
		final_pval=adjusted_pval * area
		final_kval=adjusted_kval * area
		tolerance_range_n = (1-0.05) * adjusted_nval, (1+0.05) * adjusted_nval
		tolerance_range_p = (1-0.05) * adjusted_pval, (1+0.05) * adjusted_pval
		tolerance_range_k = (1-0.05) * adjusted_kval, (1+0.05) * adjusted_kval
		recommended_n = {k:v for k, v in eq_n.items() if v[0] is not None and v[0] == crop_name if v[1] >= tolerance_range_n[0] and v[1] <= tolerance_range_n[1] }
		recommended_p = {k:v for k, v in eq_p.items() if v[0] is not None and v[0] == crop_name if v[1] >= tolerance_range_p[0] and v[1] <= tolerance_range_p[1] }
		recommended_k = {k:v for k, v in eq_k.items() if v[0] is not None and v[0] == crop_name if v[1] >= tolerance_range_k[0] and v[1] <= tolerance_range_k[1] }
		return render(request,'5. agriclinic/advisor.html',{'name':name,'crop':crop_name,'amt_nval':amt_nval_added,'amt_pval':amt_pval_added,'amt_kval':amt_kval_added,'final_nval':final_nval,'final_pval':final_pval,'final_kval':final_kval,'recommended_n':recommended_n,'recommended_p':recommended_p,'recommended_k':recommended_k,'area':area}) 
	else:
		if stage == 'Early Stage':
			adjusted_nval = (crop.stage_one_n_value / 100) * amt_nitrogen_added
			adjusted_pval = (crop.stage_one_p_value / 100) * amt_phosphorus_added
			adjusted_kval = (crop.stage_one_k_value / 100) * amt_potassium_added
		elif stage == 'Growth Stage':
			adjusted_nval = (crop.stage_two_n_value / 100) * amt_nitrogen_added
			adjusted_pval = (crop.stage_two_p_value / 100) * amt_phosphorus_added
			adjusted_kval = (crop.stage_two_k_value / 100) * amt_potassium_added
		else:
			adjusted_nval = (crop.stage_three_n_value / 100) * amt_nitrogen_added
			adjusted_pval = (crop.stage_three_p_value / 100) * amt_phosphorus_added
			adjusted_kval = (crop.stage_three_k_value / 100) * amt_potassium_added
		final_nval=adjusted_nval * area
		final_pval=adjusted_pval * area
		final_kval=adjusted_kval * area
		tolerance_range_n = (1-0.05) * adjusted_nval, (1+0.05) * adjusted_nval
		tolerance_range_p = (1-0.05) * adjusted_pval, (1+0.05) * adjusted_pval
		tolerance_range_k = (1-0.05) * adjusted_kval, (1+0.05) * adjusted_kval
		recommended_n = {k:v for k, v in eq_n.items() if v[0] is not None and v[0] == crop_name if v[1] >= tolerance_range_n[0] and v[1] <= tolerance_range_n[1] }
		recommended_p = {k:v for k, v in eq_p.items() if v[0] is not None and v[0] == crop_name if v[1] >= tolerance_range_p[0] and v[1] <= tolerance_range_p[1] }
		recommended_k = {k:v for k, v in eq_k.items() if v[0] is not None and v[0] == crop_name if v[1] >= tolerance_range_k[0] and v[1] <= tolerance_range_k[1] }
		
		return render(request,'5. agriclinic/advisor.html',{'name':name,'crop':crop_name,'amt_nval':amt_nitrogen_added,'amt_pval':amt_phosphorus_added,'amt_kval':amt_potassium_added,'final_nval':final_nval,'final_pval':final_pval,'final_kval':final_kval,'recommended_n':recommended_n,'recommended_p':recommended_p,'recommended_k':recommended_k,'area':area})

@login_required
def disease_recognition_view(request):
	if request.method == 'POST':
		form = DiseaseRecognitionForm(data=request.POST, files=request.FILES)
		if form.is_valid():
			disease_form = form.save(commit=False)
			profile = UserProfile.objects.get(user=request.user)
			disease_form.name = profile.name
			disease_form.email = request.user.email if request.user.email else None
			disease_form.phone = profile.whatsapp_no
			disease_form.state = profile.state
			disease_form.district = profile.district if profile.district else None
			disease_form.taluk = profile.taluk if profile.taluk else None
			disease_form.village = profile.village if profile.village else None
			disease_form.zone = profile.zone if profile.zone else None
			disease_form.zip_code = profile.zip_code if profile.zip_code else None
			disease_form.save()
			image_fields = ['disease_image', 'disease_image1', 'disease_image2', 'disease_image3', 'disease_image4']
			predictions = []

			for field in image_fields:
				image = getattr(disease_form, field)
				if image:
					image_url = image.url
					crop_lower = disease_form.crop.lower()
					model = tf.keras.models.load_model(f'W2AI/assets/{crop_lower}-disease-recognition.keras')
					dataset_path = f'F:/Mona/Mona-Kumari/data-sources/potato-disease-classification-model/training/{crop_lower}-dataset'
					dataset = image_dataset_from_directory(
                        dataset_path,
                        shuffle=True,
                        image_size=(256, 256),
                        batch_size=32
                    )

					response = requests.get(image_url)
					if response.status_code == 200:
						with open("downloaded_image.jpg", "wb") as f:
							f.write(response.content)
						processed_image = load_img("downloaded_image.jpg", target_size=(256, 256))
						img_array = img_to_array(processed_image)
						img_array = tf.expand_dims(img_array, 0)
						prediction = model.predict(img_array)
						predicted_class = dataset.class_names[np.argmax(prediction[0])]
						confidence = round(100 * (np.max(prediction[0])), 2)
						predictions.append({
							'image': image_url,
                            'predicted_class': predicted_class,
                            'confidence': confidence
                        })
					else:
						predictions.append({
                            'image': image_url,
                            'predicted_class': 'Error',
                            'confidence': 0
                        })

            # Save predictions to the database
			for i, prediction in enumerate(predictions):
				setattr(disease_form, f'predicted_class{i}', prediction['predicted_class'])
			disease_form.save()

			request.session['predictions'] = predictions
			return redirect(reverse('W2AI:disease-report', args=[disease_form.id]))
	else:
		form = DiseaseRecognitionForm()
	return render(request, '5. agriclinic/disease-recogition.html', {'form': form})


@login_required
def disease_report_view(request, id):
	enquiry = DiseaseRecognition.objects.get(id=id)
	predictions = request.session.get('predictions', [])
	return render(request, '5. agriclinic/disease-report.html', {'predictions': predictions, 'enquiry': enquiry})

@login_required
def update_final_prediction(request, id):
	if request.method == 'POST':
		enquiry = get_object_or_404(DiseaseRecognition, id=id)
		finalpredicted_class = request.POST.get('finalpredicted_class')
		request.session['finalpredicted_class'] = finalpredicted_class
		enquiry.finalpredicted_class = finalpredicted_class
		enquiry.save()
		return redirect(reverse('W2AI:symptom-recognition-form'))

@login_required
def symptom_recognition(request):
	if request.method == 'POST':
		form = SymptomRecognitionForm(data=request.POST)
		if form.is_valid():
			symptom_form = form.save(commit=False)
			profile = UserProfile.objects.get(user=request.user)
			symptom_form.name = profile.name
			symptom_form.whatsapp_no = profile.whatsapp_no
			symptom_form.state = profile.state
			symptom_form.email = request.user.email if request.user.email else None
			symptom_form.district = profile.district if profile.district else None
			symptom_form.taluk = profile.taluk if profile.taluk else None
			symptom_form.city = profile.city if profile.city else None
			symptom_form.save()
			instance = SymptomsRecognitionInput.objects.get(id=symptom_form.id)
			instance_crop = instance.id
			return redirect(reverse('W2AI:symptom-recognition-report', args=[instance_crop]))
	else:
		form = SymptomRecognitionForm()
	return render(request,'5. agriclinic/5.1 symptom/symptom-recognition-form.html',{'form':form})

@login_required
def symptom_recognition_report(request, id):
	symptoms = SymptomsRecognitionInput.objects.get(id=id)
	crop = symptoms.crop
	sym_knowledge = SymptomRecognitionKnowledge.objects.filter(crop=crop)
	disease_keywords={}
	deficiency_keywords={}
	pests_keywords={}
	for sym in sym_knowledge:
		if sym.disease:
			disease_keywords[sym.disease]=sym.keywords.split(',')
		elif sym.deficiencies:
			deficiency_keywords[sym.deficiencies]=sym.keywords.split(',')
		else:
			pests_keywords[sym.pests]=sym.keywords.split(',')
	keywords = symptoms.keywords
	keyword_list = keywords.split(',')
	selected_keys=[k.replace('[','').replace("'",'').replace(']','').strip() for k in keyword_list]
	selected_disease = [disease for disease, keywords_list in disease_keywords.items() for keys in selected_keys if keys in keywords_list ]
	selected_deficiency = [deficiency for deficiency, keywords_list in deficiency_keywords.items() for keys in selected_keys if keys in keywords_list ]
	selected_pests = [pests for pests, keywords_list in pests_keywords.items() for keys in selected_keys if keys in keywords_list ]
	finalpredicted_class = request.session.get('finalpredicted_class')
	predicted_disease_match = None
	if finalpredicted_class in selected_disease:
		predicted_disease_match = finalpredicted_class
	return render(request,'5. agriclinic/5.1 symptom/symptom-recognition.html',{'recognized_disease':set(selected_disease),'recognized_deficiency':set(selected_deficiency),'recognized_pests':set(selected_pests),'selected_symptoms':selected_keys,'infected_crop':crop,'predicted_disease_match': predicted_disease_match,'finalpredicted_class':finalpredicted_class})


#-------------------------------------- Above Agri Clinic Related views -------------------------------------------


#-------------------------------------- Below Nutritracker Related views -------------------------------------------
def NutriTrackerView(request):
	title=''
	desc=''
	seo = SeoContent.objects.all()
	for i in seo:
		if i.page == 'home':
			title = i.meta_title
			desc = i.meta_description
	url = request.build_absolute_uri(request.path)
	plot_data = [plot.user_profile.user.username for plot in Plot.objects.all()]
	return render(request,'6. nutritracker/nutritracker.html', {'title':title,'desc':desc,'canonical':url,'plot_data':plot_data})

from W2AI.forms import NutriTrackerModelForm

def new_user_purchase_history(request):
    if request.method == "POST":
        # Using ModelForm instead of regular Form since you're trying to save it
        form = NutriTrackerModelForm(request.POST)
        if form.is_valid():
            # Save the form data to create a new NutriTracker object
            nutritracker = form.save()
            # You can add any additional processing here if needed
            return redirect(reverse('W2AI:form-message'))  # Redirect to a success page
    else:
        # Initialize an empty form for GET requests
        form = NutriTrackerModelForm()

    return render(request, "6. nutritracker/nutritracker_form.html", {"form": form})


#########################################################################################################

def nutritracker_success(request):
    return render(request, 'nutritracker_success.html')

# class NewFarmerPurchaseHistoryViewSet(ModelViewSet):
# 	queryset = NewFarmerPurchaseHistory.objects.all()
# 	serializer_class = NewFarmerPurchaseHistorySerializer

# 	def get_ag_userinput_details(self, request):
# 		nt_newuser_hist_form = NewFarmerPurchaseHistoryForm()
# 		return render(request, 'contact.html', {'nt_newuser-hist_form': nt_newuser_hist_form})

@login_required
def sending_schedule(request):
	subject = 'Fertilizer Scheduling'
	message = 'Fertilizer Notification Scheduling'
	profile = UserProfile.objects.get(user=request.user)
	recipient_list = request.user.email if request.user.email else None
	schedule_date = NewFarmerPurchaseHistory.objects.filter(name=profile.name)
	dates = {}
	for i in schedule_date:
		if i.purchase_date1 and i.crop1 and i.crop_stage1:
			dates[str(i.purchase_date1)] = (i.crop1, i.crop_stage1)
		if i.purchase_date2 and i.crop2 and i.crop_stage2:
			dates[str(i.purchase_date2)] = (i.crop2, i.crop_stage2)
		if i.purchase_date3 and i.crop3 and i.crop_stage3:
			dates[str(i.purchase_date3)] = (i.crop3, i.crop_stage3)
		if i.purchase_date4 and i.crop4 and i.crop_stage4:
			dates[str(i.purchase_date4)] = (i.crop4, i.crop_stage4)
		if i.purchase_date5 and i.crop5 and i.crop_stage5:
			dates[str(i.purchase_date5)] = (i.crop5, i.crop_stage5) 
	date_keys = list(dates.keys())
	date_objects = [datetime.strptime(date, '%Y-%m-%d').date() for date in date_keys]
	recent_date = max(date_objects)
	data = {}
	for k, v in dates.items():
		if k == str(recent_date):
			data[recent_date] = v
	next_schedule = NutriTrackerSchedule.objects.get(crops = data[recent_date][0])
	crop_type = {
					'Annual Crops':['Amla', 'Avocado', 'Banana', 'Carrot', 'Chilli', 'Citrus', 'Cocoa', 'Coffee', 'Cotton', 'Curry Leaves', 'Dragon Fruit', 'Drumstick', 'Fig', 'Ginger', 'Grapes', 'Groundnut', 'Guava', 'Jasmin', 'Lime', 'Macadamia', 'Mahogani', 'Maize', 'Mango', 'Mangosteen', 'Mosambi', 'Onion', 'Papaya', 'Pepper', 'Pineapple', 'Potato', 'Rambutan', 'Sapota', 'Sugarcane', 'Tender Coconut', 'Tomato', 'Tur', 'Turmeric'],
					'Perennial Crops':['Areca New', 'Arecanut', 'Betelvine', 'Cashewnut', 'Cauliflower (Cole Crops)', 'Chrysanthemum', 'Coconut', 'Custard Apple', 'Durian', 'Jack Fruit', 'Kokum', 'Nutmeg', 'Paddy', 'Pomegranate', 'Rose', 'Rosewood']
			  	}
	for k, v in crop_type.items():
		if data[recent_date][0] in v:
			c_type = k
	if next_schedule.crop_types == c_type and next_schedule.crop_stage == data[recent_date][1]:
		result_date = recent_date + timedelta(days=int(next_schedule.scheduling_period)*30) 
	if datetime.today().date() == result_date:
		send_notification(subject, message, recipient_list)
	else:
		return HttpResponse("Next schedule will schedule soon")
	return HttpResponse('sent')

#FieldIntel Views
def farm_intel_view(request):
	url = request.build_absolute_uri(request.path)
	return render(request, '7. fieldintel/fieldIntel.html',{'canonical':url})


#-------------------------------------- Above Nutritracker Related views -------------------------------------------
