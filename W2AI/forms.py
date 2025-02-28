from . models import UserProfile
from django import forms
from django.contrib.auth.forms import UserCreationForm, PasswordChangeForm
from django.contrib.auth.models import User
from django.utils.safestring import mark_safe
from . models import Advisor,Plot,NutriTracker, AgriFBI, AgMachineXUserInput,AgMachineSpecifications, CropIntelInput, Feedback, AddedServices, FundRequirement, ActualSales, QtyRequirement, DiseaseRecognition, SymptomsRecognitionInput, Contact, ServiceFeedback, CropIntelKnowledge
from django.core.exceptions import ValidationError
from django.forms import inlineformset_factory,BaseInlineFormSet, RadioSelect
from django.forms import formset_factory
from .models import FBI, CropDetail

class ContactForm(forms.ModelForm):
	class Meta:
		model=Contact
		fields = '__all__'
		exclude = ['date','is_seen']
		labels={
			'comments':'Messages'
		}

		widgets = {
			'phone':forms.NumberInput(attrs={'type':'number'})
		}

class CustomUserCreationForm(UserCreationForm):
	name = forms.CharField(max_length=100,widget=forms.TextInput(attrs={'placeholder': 'Enter Your Name'}))
	whatsapp_no = forms.CharField(max_length=20, widget=forms.TextInput(attrs={'placeholder': 'Enter Your 10-digit Whatsapp Number'}))
	email = forms.EmailField(required=False, widget=forms.TextInput(attrs={'placeholder': 'Enter Your Email Id (Optional)'}))
	class Meta(UserCreationForm.Meta):
		model = User
		fields = ['name', 'whatsapp_no', 'email', 'username','password1','password2']
		widgets = {
        	'username': forms.TextInput(attrs={'placeholder': 'Enter Username'}),
        }

	def __init__(self, *args, **kwargs):
		super().__init__(*args, **kwargs)
		self.fields['password1'].widget.attrs.update({'placeholder':'Enter New Password'})
		self.fields['password2'].widget.attrs.update({'placeholder':'Confirm Password'})	

	def clean_whatsapp_no(self):
		whatsapp_no = self.cleaned_data.get("whatsapp_no")
		if len(str(whatsapp_no)) != 10:
			raise forms.ValidationError(mark_safe("<span style='color:red; font-weight: bold;'>Phone number must be of 10 digits</span>"))
		return whatsapp_no

	def save(self, commit=True):
		user = super().save(commit=False)
		user_profile = UserProfile(user=user, whatsapp_no=self.cleaned_data['whatsapp_no'], name=self.cleaned_data['name'], email=self.cleaned_data['email'])
		if commit:
			user.save()
			user_profile.save()
		return user
        
class LoginForm(forms.Form):
    username = forms.CharField()
    password = forms.CharField(widget=forms.PasswordInput())

class CustomPasswordChangeForm(PasswordChangeForm):
    def clean_new_password(self):
        password = self.cleaned_data.get("new_password")
        user = self.user
        
        if len(password) < 6:
            raise forms.ValidationError("<span style='color:red; font-weight: bold;'>Password Length should be at least 6</span>")
        
        password_lower = password.lower()
        username = user.username.lower()
        name = user.get_full_name().lower()
        
        if username in password_lower or name in password_lower:
            raise forms.ValidationError("<span style='color:red; font-weight: bold;'>Password should not contain your name or username</span>")
        
        elif (username in name or name in username) and any(part in password_lower for part in (username, name)):
            raise forms.ValidationError("<span style='color:red; font-weight: bold;'>Password should not contain your name or username</span>")
        
        elif password_lower.isdigit() or password_lower.isalpha():
            raise forms.ValidationError("<span style='color:red; font-weight: bold;'>Password should not contain only digits or letters</span>")
        
        return password
    
class AdvisorForm(forms.ModelForm):
    class Meta:
        model = Advisor
        exclude = ['user']  # Exclude the 'user' field as it's handled programmatically
        labels = {
            'full_name': 'Full Name',
            'whatsapp_no': 'WhatsApp Number',
            'email': 'Email Address',
            'crop_area': 'Land Area (in Acres)',
            'crop': 'Select Crop',
            'ph_value': 'pH Value in Soil Test Report',
            'n_value': 'N Value in Soil Test Report',
            'p_value': 'P Value in Soil Test Report',
            'k_value': 'K Value in Soil Test Report',
            'crop_stage': 'Crop Stage',
            'village': 'Village',
            'taluk': 'Taluk',
            'district': 'District',
            'state': 'State',
            'zip_code': 'Zip Code',
            'land_area': 'Land Area',
            'zone': 'Agricultural Zone',
        }
        widgets = {
            'crop': forms.Select(attrs={'class': 'form-control'}),
            'crop_stage': forms.Select(attrs={'class': 'form-control'}),
            'ph_value': forms.NumberInput(attrs={'class': 'form-control', 'step': '0.1'}),
            'n_value': forms.NumberInput(attrs={'class': 'form-control', 'step': '0.1'}),
            'p_value': forms.NumberInput(attrs={'class': 'form-control', 'step': '0.1'}),
            'k_value': forms.NumberInput(attrs={'class': 'form-control', 'step': '0.1'}),
            'full_name': forms.TextInput(attrs={'class': 'form-control'}),
            'whatsapp_no': forms.TextInput(attrs={'class': 'form-control', 'maxlength': '10'}),
            'email': forms.EmailInput(attrs={'class': 'form-control'}),
            'village': forms.TextInput(attrs={'class': 'form-control'}),
            'taluk': forms.TextInput(attrs={'class': 'form-control'}),
            'district': forms.TextInput(attrs={'class': 'form-control'}),
            'state': forms.TextInput(attrs={'class': 'form-control'}),
            'zip_code': forms.TextInput(attrs={'class': 'form-control'}),
            'land_area': forms.TextInput(attrs={'class': 'form-control'}),
            'zone': forms.TextInput(attrs={'class': 'form-control'}),
        }


# class AgMachineXUserInputForm(forms.ModelForm):
# 	class Meta:
# 		model = AgMachineXUserInput
# 		fields = ['machinery_req','land_area','machine_available', 'labours_employed', 'irrigation_req','other_current_irrigation','water_source','water_availability', 'soil_condition','budget','vegetation_type']
from django import forms
from .models import AgMachineXUserInput

class AgMachineXUserInputForm(forms.ModelForm):
    class Meta:
        model = AgMachineXUserInput
        fields = [
            'full_name', 'whatsapp_no', 'email_id', 'village', 'taluk', 'district', 'state', 'zip_code',
            'land_area', 'zone', 'soil_condition', 'labours_employed', 'crop', 'crop_stage',
            'machinery_req', 'soil_type', 'machine_available', 'irrigation_type', 'water_source',
            'water_availability', 'current_irrigation_method', 'other_current_irrigation',
            'irrigation_req', 'budget', 'vegetation_type'
        ]
        
        widgets = {
            'full_name': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Enter full name'}),
            'whatsapp_no': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Enter WhatsApp number'}),
            'email_id': forms.EmailInput(attrs={'class': 'form-control', 'placeholder': 'Enter email'}),
            'village': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Enter village'}),
            'taluk': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Enter taluk'}),
            'district': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Enter district'}),
            'state': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Enter state'}),
            'zip_code': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Enter ZIP code'}),
            'land_area': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Enter land area'}),
            'zone': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Enter zone'}),
            'soil_condition': forms.Select(attrs={'class': 'form-control'}),
            'labours_employed': forms.NumberInput(attrs={'class': 'form-control'}),
            'crop': forms.Select(attrs={'class': 'form-control'}),
            'crop_stage': forms.Select(attrs={'class': 'form-control'}),
            'machinery_req': forms.Select(attrs={'class': 'form-control'}),
            'soil_type': forms.Select(attrs={'class': 'form-control'}),
            'machine_available': forms.Select(attrs={'class': 'form-control'}),
            'irrigation_type': forms.Select(attrs={'class': 'form-control'}),
            'water_source': forms.TextInput(attrs={'class': 'form-control'}),
            'water_availability': forms.TextInput(attrs={'class': 'form-control'}),
            'current_irrigation_method': forms.Select(attrs={'class': 'form-control'}),
            'other_current_irrigation': forms.Textarea(attrs={'class': 'form-control', 'rows': 3}),
            'irrigation_req': forms.Select(attrs={'class': 'form-control'}),
            'budget': forms.Select(attrs={'class': 'form-control'}),
            'vegetation_type': forms.Select(attrs={'class': 'form-control'}),
        }

class AgMachinexFilterForm(forms.Form):
    def __init__(self, *args, **kwargs):
        super(AgMachinexFilterForm, self).__init__(*args, **kwargs)
        self.fields['brand'].choices = self.get_brand_choices()
        self.fields['crop'].choices = self.get_crop_choices()

    def get_brand_choices(self):
        brands = AgMachineSpecifications.objects.values_list('brand', flat=True).distinct()
        return [(brand, brand) for brand in brands]
    
    def get_crop_choices(self):
        crops = AgMachineSpecifications.objects.values_list('crop', flat=True).distinct()
        return [(crop, crop) for crop in crops]
    
    brand = forms.ChoiceField(label='Brand', choices=[], widget=forms.RadioSelect, required=False)
    crop = forms.ChoiceField(label='Crop', choices=[], widget=forms.RadioSelect, required=False)


class UserProfileForm(forms.ModelForm):
	class Meta:
		model = UserProfile
		fields = ['zone_district','taluk', 'village']
		labels = {
        	'zone_district': 'Select the District[Location] where the crop is grown',
            'taluk': 'Select Taluk /ತಾಲೂಕು ಆಯ್ಕೆ',
            'village': 'Enter your Village',
        }

	
PlotFormSet = inlineformset_factory(
	UserProfile,
	Plot,
	fields=['plot_name', 'crop_grown', 'land_area', 'soil_condition', 'soil_health', 'soil_ph', 'soil_rich_nutrients', 'soil_average_nutrients', 'soil_poor_nutrients', 'water_source', 'water_availability'],
	extra=5, 
	can_delete=True, 
)
    
class CropIntelUserInputForm(forms.ModelForm):
	planting_date = forms.DateField(
		widget=forms.DateInput(attrs={'type': 'date'})  # This will render a date picker in modern browsers
        )
	class Meta:
		model = CropIntelInput
		fields = ['land_type','cultivation','crop_varieties','no_of_plants','spacing','crop_stage','land_prepration','inter_crops','crop_yield','planting_date','pests','diseases','planting_method']
        
		labels = {
            'land_type':'Select Land Type',
            'cultivation':'Cultivation since 5 years',
            'land_prepration':'Land Preparation Needed',
            'crop_yield':'Crop yield (qty in kgs)',
            'inter_crops':'Select if any Inter crop you are planning to cultivate?',
            'crop_varieties':'Crop Variety Grown'
        }
		widgets = {
            'crop_varieties': forms.Select(choices=[('', 'Select Crop Varieties')] + list(CropIntelInput.VARIETIES)),
            'no_of_plants': forms.NumberInput(attrs={'placeholder': 'Enter The Number Of Plants.'}),
            'spacing':forms.TextInput(attrs={'placeholder': 'Enter the Spacing eg:19*19.'}),            
            'crop_stage': forms.Select(choices=[('', 'Select crop stage')] + list(CropIntelInput.STAGES)),
            'land_preparation': forms.Select(choices=[('', 'Select if land preparation is needed')] + list(CropIntelInput.LAND_PREPARATION)),
            'inter_crops': forms.Select(choices=[('', 'Select Intercrop you are planning')] + list(CropIntelInput.CROPS)),
            'crop_yield': forms.NumberInput(attrs={'placeholder': 'Enter the expected crop yield (quantity in kgs).'}),
            'pests': forms.Select(choices=[('', 'Any Pests In Crop')] + list(CropIntelInput.PESTS)),
            'diseases': forms.Select(choices=[('', 'Any Diseases in crop')] + list(CropIntelInput.DISEASES)),
            'planting_date': forms.DateInput(attrs={'placeholder': 'Select The Date When Planting Was Done.'}),
           
	}
        
class FundRequirementForm(forms.ModelForm):
    amount_jan = forms.FloatField(label='Fund (Rs.) Req. in January', required=False, widget=forms.NumberInput(attrs={'step': 'any'}))
    amount_feb = forms.FloatField(label='Fund (Rs.) Req. in February', required=False, widget=forms.NumberInput(attrs={'step': 'any'}))
    amount_mar = forms.FloatField(label='Fund (Rs.) Req. in March', required=False, widget=forms.NumberInput(attrs={'step': 'any'}))
    amount_apr = forms.FloatField(label='Fund (Rs.) Req. in April', required=False, widget=forms.NumberInput(attrs={'step': 'any'}))
    amount_may = forms.FloatField(label='Fund (Rs.) Req. in May', required=False, widget=forms.NumberInput(attrs={'step': 'any'}))
    amount_jun = forms.FloatField(label='Fund (Rs.) Req. in June', required=False, widget=forms.NumberInput(attrs={'step': 'any'}))
    amount_jul = forms.FloatField(label='Fund (Rs.) Req. in July', required=False, widget=forms.NumberInput(attrs={'step': 'any'}))
    amount_aug = forms.FloatField(label='Fund (Rs.) Req. in August', required=False, widget=forms.NumberInput(attrs={'step': 'any'}))
    amount_sep = forms.FloatField(label='Fund (Rs.) Req. in September', required=False, widget=forms.NumberInput(attrs={'step': 'any'}))
    amount_oct = forms.FloatField(label='Fund (Rs.) Req. in October', required=False, widget=forms.NumberInput(attrs={'step': 'any'}))
    amount_nov = forms.FloatField(label='Fund (Rs.) Req. in November', required=False, widget=forms.NumberInput(attrs={'step': 'any'}))
    amount_dec = forms.FloatField(label='Fund (Rs.) Req. in December', required=False, widget=forms.NumberInput(attrs={'step': 'any'}))
    class Meta:
        model = FundRequirement
        fields = ['crops','crop_varieties','quantity_available','amount_jan','amount_feb','amount_mar','amount_apr','amount_may','amount_jun','amount_jul','amount_aug','amount_sep','amount_oct','amount_nov','amount_dec']
        labels = {
            'crops':'Select Crop',
            'crop_varieties':'Select Variety of crop',
        }

class QtyRequirementForm(forms.ModelForm):
    amount_jan = forms.FloatField(label='Fund (Rs.) Available in January', required=False, widget=forms.NumberInput(attrs={'step': 'any'}))
    amount_feb = forms.FloatField(label='Fund (Rs.) Available in February', required=False, widget=forms.NumberInput(attrs={'step': 'any'}))
    amount_mar = forms.FloatField(label='Fund (Rs.) Available in March', required=False, widget=forms.NumberInput(attrs={'step': 'any'}))
    amount_apr = forms.FloatField(label='Fund (Rs.) Available in April', required=False, widget=forms.NumberInput(attrs={'step': 'any'}))
    amount_may = forms.FloatField(label='Fund (Rs.) Available in May', required=False, widget=forms.NumberInput(attrs={'step': 'any'}))
    amount_jun = forms.FloatField(label='Fund (Rs.) Available in June', required=False, widget=forms.NumberInput(attrs={'step': 'any'}))
    amount_jul = forms.FloatField(label='Fund (Rs.) Available in July', required=False, widget=forms.NumberInput(attrs={'step': 'any'}))
    amount_aug = forms.FloatField(label='Fund (Rs.) Available in August', required=False, widget=forms.NumberInput(attrs={'step': 'any'}))
    amount_sep = forms.FloatField(label='Fund (Rs.) Available in September', required=False, widget=forms.NumberInput(attrs={'step': 'any'}))
    amount_oct = forms.FloatField(label='Fund (Rs.) Available in October', required=False, widget=forms.NumberInput(attrs={'step': 'any'}))
    amount_nov = forms.FloatField(label='Fund (Rs.) Available in November', required=False, widget=forms.NumberInput(attrs={'step': 'any'}))
    amount_dec = forms.FloatField(label='Fund (Rs.) Available in December', required=False, widget=forms.NumberInput(attrs={'step': 'any'}))
    class Meta:
        model = QtyRequirement
        fields = ['crops','crop_varieties','quantity_required','amount_jan','amount_feb','amount_mar','amount_apr','amount_may','amount_jun','amount_jul','amount_aug','amount_sep','amount_oct','amount_nov','amount_dec']
        labels = {
            'crops':'Select Crop',
            'crop_varieties':'Select Variety of crop',
            'quantity_req':'Quantity Required',
        }

class ActualSalesForm(forms.ModelForm):
    amount_jan = forms.FloatField(label='Price Realised in January', required=False, widget=forms.NumberInput(attrs={'step': 'any'}))
    amount_feb = forms.FloatField(label='Price Realised in February', required=False, widget=forms.NumberInput(attrs={'step': 'any'}))
    amount_mar = forms.FloatField(label='Price Realised in March', required=False, widget=forms.NumberInput(attrs={'step': 'any'}))
    amount_apr = forms.FloatField(label='Price Realised in April', required=False, widget=forms.NumberInput(attrs={'step': 'any'}))
    amount_may = forms.FloatField(label='Price Realised in May', required=False, widget=forms.NumberInput(attrs={'step': 'any'}))
    amount_jun = forms.FloatField(label='Price Realised in June', required=False, widget=forms.NumberInput(attrs={'step': 'any'}))
    amount_jul = forms.FloatField(label='Price Realised in July', required=False, widget=forms.NumberInput(attrs={'step': 'any'}))
    amount_aug = forms.FloatField(label='Price Realised in August', required=False, widget=forms.NumberInput(attrs={'step': 'any'}))
    amount_sep = forms.FloatField(label='Price Realised in September', required=False, widget=forms.NumberInput(attrs={'step': 'any'}))
    amount_oct = forms.FloatField(label='Price Realised in October', required=False, widget=forms.NumberInput(attrs={'step': 'any'}))
    amount_nov = forms.FloatField(label='Price Realised in November', required=False, widget=forms.NumberInput(attrs={'step': 'any'}))
    amount_dec = forms.FloatField(label='Price Realised in December', required=False, widget=forms.NumberInput(attrs={'step': 'any'}))
    quant_jan = forms.FloatField(label='Quantity Released in January', required=False, widget=forms.NumberInput(attrs={'step': 'any'}))
    quant_feb = forms.FloatField(label='Quantity Released in February', required=False, widget=forms.NumberInput(attrs={'step': 'any'}))
    quant_mar = forms.FloatField(label='Quantity Released in March', required=False, widget=forms.NumberInput(attrs={'step': 'any'}))
    quant_apr = forms.FloatField(label='Quantity Released in April', required=False, widget=forms.NumberInput(attrs={'step': 'any'}))
    quant_may = forms.FloatField(label='Quantity Released in May', required=False, widget=forms.NumberInput(attrs={'step': 'any'}))
    quant_jun = forms.FloatField(label='Quantity Released in June', required=False, widget=forms.NumberInput(attrs={'step': 'any'}))
    quant_jul = forms.FloatField(label='Quantity Released in July', required=False, widget=forms.NumberInput(attrs={'step': 'any'}))
    quant_aug = forms.FloatField(label='Quantity Released in August', required=False, widget=forms.NumberInput(attrs={'step': 'any'}))
    quant_sep = forms.FloatField(label='Quantity Released in September', required=False, widget=forms.NumberInput(attrs={'step': 'any'}))
    quant_oct = forms.FloatField(label='Quantity Released in October', required=False, widget=forms.NumberInput(attrs={'step': 'any'}))
    quant_nov = forms.FloatField(label='Quantity Released in November', required=False, widget=forms.NumberInput(attrs={'step': 'any'}))
    quant_dec = forms.FloatField(label='Quantity Released in December', required=False, widget=forms.NumberInput(attrs={'step': 'any'}))
    
    class Meta:
        model = ActualSales
        fields = ['crops','crop_varieties','amount_jan','amount_feb','amount_mar','amount_apr','amount_may','amount_jun','amount_jul','amount_aug','amount_sep','amount_oct','amount_nov','amount_dec', 'quant_jan','quant_feb','quant_mar','quant_apr','quant_may','quant_jun','quant_jul','quant_aug','quant_sep','quant_oct','quant_nov','quant_dec']
        labels = {
            'crops':'Select Crop',
            'crop_varieties':'Select Variety of crop',
        }

class FeedbackForm(forms.ModelForm):
    class Meta:
        model = Feedback
        fields = '__all__'

    def clean_mobile_no(self):
        mobile_no = self.cleaned_data.get("mobile_no")
        if len(str(mobile_no)) != 10:
            raise forms.ValidationError(mark_safe("<span style='color:red; font-weight: bold;'>Phone number must be of 10 digits</span>"))
        return mobile_no
    
class FeedbackFormset(BaseInlineFormSet):
    def __init__(self, *args, **kwargs):
        service_choices = ServiceFeedback.SERVICES
        super().__init__(*args, **kwargs)
        if service_choices:
            for i, form in enumerate(self.forms):
                if i <= len(service_choices):
                    form.fields['services_used'].widget.choices = [(service_choices[i][0], service_choices[i][1])]
                else:
                    form.empty_permitted = False
                    form.fields['team_activity'].widget = forms.HiddenInput()

def get_feedback_formset(extra_forms):
    return inlineformset_factory(
        Feedback,
        ServiceFeedback,
        formset = FeedbackFormset,
        fields=['services_used','rating','feedback','suggestions'],
        extra=extra_forms,
        can_delete=True,
        widgets={
            'services_used':RadioSelect(attrs={'class':'radio'}),
        }
    )


class AddedServiceForm(forms.ModelForm):
    class Meta:
        model = AddedServices
        fields = '__all__'
        labels = {
            'farm_size':'Farm Size (in Acre)',
            'current_farm_tech':'Current Farming Practices Adopted',
            'challenges':'Specific Challenges Faced',
        }

    def clean_mobile_no(self):
        mobile_no = self.cleaned_data.get("mobile_no")
        if len(str(mobile_no)) != 10:
            raise forms.ValidationError(mark_safe("<span style='color:red; font-weight: bold;'>Phone number must be of 10 digits</span>"))
        return mobile_no
    
class DiseaseRecognitionForm(forms.ModelForm):
	class Meta:
		model = DiseaseRecognition
		fields = ['crop','disease_image','disease_image1','disease_image2','disease_image3','disease_image4']
		labels = {
            'disease_image':'Upload Crop Leaf Image 1 ',
            'disease_image1':'Upload Crop Leaf Image 2 ',
            'disease_image2':'Upload Crop Leaf Image 3 ',
            'disease_image3':'Upload Crop Leaf Image 4 ',
            'disease_image4':'Upload Crop Leaf Image 5',

		}

class SymptomRecognitionForm(forms.ModelForm):
    keywords = forms.MultipleChoiceField(widget=forms.CheckboxSelectMultiple, choices=SymptomsRecognitionInput.KEYWORD_CHOICES)
    class Meta:
        model = SymptomsRecognitionInput
        fields = ['crop','keywords']

class CustomPlaceholderTextInput(forms.TextInput):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.attrs['style'] = 'font-size: 13px;'

class CustomPlaceholderTextarea(forms.Textarea):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.attrs['style'] = 'font-size: 13px;'
        

class CropIntelKnowledgeForm(forms.ModelForm):
	class Meta:
		model = CropIntelKnowledge
		fields = '__all__'
    
	def __init__(self, *args, **kwargs):
		super().__init__(*args, **kwargs)
		self.fields['area_zone'].widget.attrs.update({'class': 'horizontal-multiselect'})
		self.fields['propagation_method'].widget.attrs.update({'class': 'horizontal-multiselect'})
		self.fields['soil_type'].widget.attrs.update({'class': 'horizontal-multiselect'})
		self.fields['inter_crops'].widget.attrs.update({'class': 'horizontal-multiselect'})
          

class NutriTrackerForm(forms.Form):
    # Your Information
    name = forms.CharField(label="Your Name", max_length=100)
    whatsapp_number = forms.CharField(label="WhatsApp Number", max_length=15)
    district = forms.CharField(label="District", max_length=100)
    taluk = forms.CharField(label="Taluk", max_length=100)
    address = forms.CharField(label="Address", widget=forms.Textarea(attrs={'rows': 3}))
    extent_of_land = forms.FloatField(label="Extent of Land (in Acres)")

    # Plot Information
    plot_name = forms.CharField(label="Plot Name", max_length=100)
    crop_grown = forms.ChoiceField(label="Crop Grown", choices=NutriTracker.CROP_CHOICES)
    land_area = forms.FloatField(label="Land Area (Acres)")
    crop_density = forms.IntegerField(label="Crop Density (No. of Plants/Acre)")

    # Soil Information
    soil_condition = forms.ChoiceField(label="Soil Condition", choices=NutriTracker.SOIL_CONDITION_CHOICES)
    soil_health = forms.ChoiceField(label="Soil Health", choices=NutriTracker.SOIL_HEALTH_CHOICES)
    soil_ph = forms.FloatField(label="Soil pH")
    water_source = forms.ChoiceField(label="Water Source", choices=NutriTracker.WATER_SOURCE_CHOICES)
    water_availability = forms.ChoiceField(label="Water Availability", choices=NutriTracker.WATER_AVAILABILITY_CHOICES)
    soil_rich_nutrients = forms.ChoiceField(label="Soil Rich Nutrients", choices=NutriTracker.NUTRIENT_CHOICES, required=False)
    soil_avg_nutrients = forms.ChoiceField(label="Soil Average Nutrients", choices=NutriTracker.NUTRIENT_CHOICES, required=False)
    soil_poor_nutrients = forms.ChoiceField(label="Soil Poor Nutrients", choices=NutriTracker.NUTRIENT_CHOICES, required=False)

    # Cultivation Information
    sowing_month = forms.ChoiceField(label="Select Sowing/Planting Month", choices=NutriTracker.MONTH_CHOICES)
    harvesting_month = forms.ChoiceField(label="Select Expected Harvesting Month", choices=NutriTracker.MONTH_CHOICES)
    irrigation_method = forms.ChoiceField(label="Select Irrigation Method Adopted", choices=NutriTracker.IRRIGATION_METHOD_CHOICES)
    nutrient_application_times = forms.IntegerField(label="No. of Times Nutrients Applied (per Year)")

    # Soil Test Report Values
    nitrogen_value = forms.FloatField(label="Enter Nitrogen (N) Value")
    potassium_value = forms.FloatField(label="Enter Potassium (P) Value")
    phosphorous_value = forms.FloatField(label="Enter Phosphorous (K) Value")
    secondary_nutrients_value = forms.FloatField(label="Enter Secondary Nutrients Value")
    micronutrients_value = forms.FloatField(label="Enter Micronutrients Value")
    organic_carbon_value = forms.FloatField(label="Enter Organic Carbon (C) Value")

    # Fertilizer Purchase Details
    crop_fertilizer_applied = forms.ChoiceField(label="Select Crop for which Fertilizer Applied", choices=NutriTracker.CROP_CHOICES)
    crop_stage = forms.ChoiceField(label="Select Crop Stage at which Fertilizer Applied", choices=NutriTracker.CROP_STAGE_CHOICES)
    fertilizer_name = forms.CharField(label="Enter Fertilizer Name", max_length=100)
    nutrient_deficiency = forms.ChoiceField(label="Select for which nutrient deficiency Fertilizer Applied", choices=NutriTracker.NUTRIENT_CHOICES)
    fertilizer_type = forms.ChoiceField(label="Select Which Type of Fertilizer Applied", choices=NutriTracker.FERTILIZER_TYPE_CHOICES)
    manufacturer_name = forms.CharField(label="Enter Manufacturer Name", max_length=100)
    fertilizer_quantity = forms.FloatField(label="Enter Quantity of Fertilizer Applied")
    fertilizer_purchase_date = forms.DateField(
        label="Select Date of Purchase",
        widget=forms.DateInput(attrs={'type': 'date'})
    )


class NutriTrackerModelForm(forms.ModelForm):
    class Meta:
        model = NutriTracker
        fields = '__all__'
        widgets = {
            'address': forms.Textarea(attrs={'rows': 3}),
            'fertilizer_purchase_date': forms.DateInput(attrs={'type': 'date'}),
        }

class FBIForm(forms.ModelForm):
    class Meta:
        model = FBI
        fields = [
            'name', 'whatsapp_number', 'district', 'taluk', 
            'address', 'land_extent', 'user_type'
        ]
        labels = {
            'name': 'Name',
            'whatsapp_number': 'WhatsApp Number',
            'district': 'District',
            'taluk': 'Taluk',
            'address': 'Address',
            'land_extent': 'Extent of Land',
            'user_type': 'User'
        }
        widgets = {
            'address': forms.Textarea(attrs={'rows': 3, 'style': 'width: 100%;'}),
            'user_type': forms.Select(choices=FBI.USER_CHOICES)
        }

class CropDetailForm(forms.ModelForm):
    class Meta:
        model = CropDetail
        fields = ['crop_name', 'crop_quantity', 'crop_variety']
        labels = {
            'crop_name': 'Crop Name',
            'crop_quantity': 'Quantity (Quintal)',
            'crop_variety': 'Crop Variety Name'
        }
        widgets = {
            'crop_name': forms.Select(choices=CropDetail.CROP_CHOICES)
        }

# Create a formset for handling multiple crop details
CropDetailFormSet = formset_factory(
    CropDetailForm,
    extra=1,  # Start with one form
    can_delete=True  # Allow deletion of forms
)
