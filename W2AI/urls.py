from django.conf import settings
from django.contrib import admin 
from django.urls import path, include
from . import views 
from django.contrib.auth.views import LogoutView
from rest_framework.routers import DefaultRouter

from django.conf.urls.static import static


app_name='W2AI'

router=DefaultRouter()
router.register(r'feedback',views.FeedbackViewSet, basename='feedback')
router.register(r'custom-service',views.addedServiceViewSet, basename='custom-service')
router.register(r'agmachinex-user-input',views.AgMachineXUserInputViewSet, basename='agmachinex-user-input')
router.register(r'agmachinex-specifications',views.AgMachineSpecificationsView, basename='agmachinex-specifications')
router.register(r'crop-intel-knowledge',views.CropIntelKnowledgeView, basename='crop-intel-knowledge')
router.register(r'fbi-report',views.FBIReportsView, basename='fbi-report')
router.register(r'contact-us-messages',views.contactusViewSet, basename='contact-us')

urlpatterns = [
    path("admin/", admin.site.urls),
    path('api/',include(router.urls)),
    path('', views.HomeView,name="home"),
    path('about-us/', views.AboutView,name="aboutus"),
    path('contact-us/', views.contact,name="contactus"),
    path('contact-acknowledgment',views.thankyou,name='contactack'),
    path('register/', views.register_view, name='register_url'),
    path('login/', views.login_view, name='login_url'),
    path('logout/',views.logout_view,name="logout"),
	path('get-location/',views.get_location, name='get-location'),
    path('dashboard/',views.dashboardView, name="dashboard"),
    path('update-user-profile/', views.user_profile_view, name='update-user-profile'),
    path('change-password/',views.changePasswordView, name='change_password'),
    path('change-password/done/',views.password_change_done, name='password_change_done'),
    path('delete-plot/<int:plot_id>/', views.delete_plot, name='delete_plot'),
    path('submit-contact/', views.handle_contact_form, name='submit_contact'),
    path('nutri-tracker/', views.NutriTrackerView,name="nutritracker"),
    # path('nutri-tracker-input-form/', views.new_user_purchase_history,name='nutri-tracker-input-form'),
    path('nutritracker_form/', views.new_user_purchase_history,name='nutritracker_form'),
    path('ag-machine-x/', views.AgMachineXView,name="agmachinex"),
    path('agmachinex-input-form/', views.agmachinex_user_input_view, name='agmachinex-input-form'),
    path('agmachinex-recommendation/<int:instance_id>/', views.agmachinex_recommendation_view, name='agmachinex-recommendation'),
    path('market-planner-fund-requirement/<str:user_type>/', views.fund_requirement, name="fund-requirement"),
	path('external-links/',views.BacklinksView,name='external-links'),


    #CropIntel URLs
    path('crop-intel/', views.CropIntelView,name="cropintel"),
    path('crop-intel-user-input-Form/', views.crop_intel_feeding_form, name='crop-intel-form'),
    path('crop-intel-recommendation',views.crop_intel_recommendation, name='crop-intel-recommendation'),
    path('agri-clinic/', views.AgriClinicView,name="agriclinic"),
    path('advisor_form/',views.advisor_view,name='advisor_form'),
    path('nutrient-recommended/<str:crop_name>/<int:id>/',views.amt_of_nutrient,name='nutrient-recommendation'),
	path('agri-fbi/', views.FBIView,name="agri-fbi"),  
    path('agri-fbi-crop-select/', views.fbi_form, name='fbi-crop-selection'),
    path('agri-fbi-report-generation/<int:instance_id>/', views.fbi_report_generate, name='fbi-report-generation'),
    path('fund-requirement-enquiry',views.fund_requirement, name='fund-requirement'),
    path('qunatity-requirement-enquiry',views.qty_requirement, name='qty-requirement'),
    path('market-planner-market-planner',views.market_planner, name='market-planner-strategies'),
    path('actual-sales-storage', views.actual_sales, name='actual-sales'),

    path('agriclinic/symptom-recognition-form/', views.symptom_recognition, name='symptom-recognition-form'),
    path('agriclinic/symptom-recognition/<int:id>/',views.symptom_recognition_report, name='symptom-recognition-report'),
    path('disease-recognition-enquiry',views.disease_recognition_view, name='disease-recognition'),
    path('disease-report/<int:id>/',views.disease_report_view, name='disease-report'),
	path('update-final-prediction/<int:id>/', views.update_final_prediction, name='update_final_prediction'),
    path('schedule/', views.sending_schedule, name='schedule'),
    path('field-intel/', views.farm_intel_view, name='field-intel'),
    path('user-feedback/',views.feedback_view, name='feedback'),
	path('feedback-success/',views.feedback_success_view, name="feedback-success"),
    path('farm-management-solutions/',views.added_service_view, name='custom-service'),
	path('enquiry-success-message/', views.form_submission_success_message_view, name='form-message')
]

if settings.DEBUG:
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)