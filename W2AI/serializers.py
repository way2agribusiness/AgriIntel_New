from rest_framework import serializers
from .models import Feedback, AddedServices, Contact, AgMachineXUserInput, AgMachineSpecifications, NutriTracker, CropIntelKnowledge, AgriFBI, CurrentMonthReport, SeasonalReport, LastMonthReport

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

# class NewFarmerPurchaseHistorySerializer(serializers.ModelSerializer):
#     class Meta:
#         model = NewFarmerPurchaseHistory
#         fields = '__all__'

class NutriTrackerSerializer(serializers.ModelSerializer):
    class Meta:
        model = NutriTracker
        fields = '__all__'

# class ExistingFarmerPurchaseHistorySerializer(serializers.ModelSerializer):
#     nutri_tracker = NutriTrackerSerializer()
#     class Meta:
#         model = ProductPurchased
#         fields = '__all__'

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
