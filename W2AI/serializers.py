from rest_framework import serializers
from .models import Feedback, AddedServices, Contact, AgMachineXUserInput,NewFarmerPurchaseHistory, AgMachineSpecifications, NutriTracker, ProductPurchased, CropIntelKnowledge, AgriFBI, CurrentMonthReport, SeasonalReport, LastMonthReport
from .models import ATSInfo, ATSContactInfo, ATSIntro, ATSContactProductInfo, ATSSeller, ATSContactProductImages

class FeedbackSerializer(serializers.ModelSerializer):
    class Meta:
        model = Feedback
        fields = '__all__'

class AddedServicesSerializer(serializers.ModelSerializer):
    class Meta:
        model = AddedServices
        fields = '__all__'

class ContactSerializer(serializers.ModelSerializer):
    class Meta:
        model = Contact
        fields = '__all__'

class AgMachineXUserInputSerializer(serializers.ModelSerializer):
    class Meta:
        model = AgMachineXUserInput
        fields = '__all__'

class AgMachineSpecificationsSerializer(serializers.ModelSerializer):
    product_image = serializers.ImageField(use_url=True)
    class Meta:
        model = AgMachineSpecifications
        fields = '__all__'

class NewFarmerPurchaseHistorySerializer(serializers.ModelSerializer):
    class Meta:
        model = NewFarmerPurchaseHistory
        fields = '__all__'

class NutriTrackerSerializer(serializers.ModelSerializer):
    class Meta:
        model = NutriTracker
        fields = '__all__'

class ExistingFarmerPurchaseHistorySerializer(serializers.ModelSerializer):
    nutri_tracker = NutriTrackerSerializer()
    class Meta:
        model = ProductPurchased
        fields = '__all__'

class CropIntelKnowledgeSerializer(serializers.ModelSerializer):
    crop_variety_image = serializers.ImageField(use_url=True)
    class Meta:
        model = CropIntelKnowledge
        fields = '__all__'

class CurrentReportFBISerializer(serializers.ModelSerializer):
    class Meta:
        model = CurrentMonthReport
        fields = '__all__'

class FBISerializer(serializers.ModelSerializer):
    current_report = CurrentReportFBISerializer
    crop_image = serializers.ImageField(use_url=True)
    class Meta:
        model = AgriFBI
        fields = '__all__'

class LastMonthReportFBISerializer(serializers.ModelSerializer):
    class Meta:
        model = LastMonthReport
        fields = '__all__'

class SeasonalReportFBISerializer(serializers.ModelSerializer):
    class Meta:
        model = SeasonalReport
        fields = '__all__'

class FBISerializer(serializers.ModelSerializer):
    current_month_report = CurrentReportFBISerializer()
    last_month_report = LastMonthReportFBISerializer()
    seasonal_report = SeasonalReportFBISerializer()
    crop_image = serializers.ImageField(use_url=True)
    class Meta:
        model = AgriFBI
        fields = '__all__'

class ATSIntroSerializer(serializers.ModelSerializer):
    class Meta:
        model = ATSIntro
        fields = '__all__'

class ATSSerializer(serializers.ModelSerializer):
    category_image = serializers.ImageField(use_url=True)
    class Meta:
        model = ATSInfo
        fields = '__all__' 
    
class ATSContactSerializer(serializers.ModelSerializer):
	contact_company_logo = serializers.ImageField(use_url=True)
	class Meta:
		model = ATSContactInfo
		fields = '__all__'

	def to_representation(self, instance):
		data = super().to_representation(instance)
		if self.context['request'].method == 'POST':
			return data
		else:
			data['category'] = ATSSerializer(instance.category).data
			return data
    
class ATSContactProductSerializer(serializers.ModelSerializer):
    seller = ATSContactSerializer('seller')

    class Meta:
        model = ATSContactProductInfo
        fields = '__all__' 

class ATSContactProductImagesSerializer(serializers.ModelSerializer):
    seller = ATSContactSerializer('seller')
    seller_product = ATSContactProductSerializer()
    product_image = serializers.ImageField(use_url=True)

    class Meta:
        model = ATSContactProductImages
        fields = '__all__'


