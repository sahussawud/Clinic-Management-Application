from django.urls import path  
from Treatment import views
  
urlpatterns = [ 
    path('patient/', views.home_patient, name = 'home_patient'),
    path('patient/find/', views.find_patient, name = 'find_patient'),
    path('patient/create/', views.create_patient, name = 'create_patient'),
    path('patient/update/<int:patient_id>/', views.update_patient, name = 'update_patient'),
    path('patient/update/cd/', views.Conginetal_diseaseWithoutPatientAPIView.as_view(), name='cd_api'),
    path('patient/update/<int:patient_id>/cd_api/', views.Conginetal_diseaseAPIView.as_view(), name='cd_api'),
    path('patient/update/drug/', views.DrugWithoutPatientAPIView.as_view(), name='drug_api'),
    path('patient/search/', views.PatientSearchAPIView.as_view(), name='patient_api'),
    path('patient/search/<int:patient_id>/', views.PatientAPIView.as_view(), name='patient_api'),
    path('patient/update/<int:patient_id>/drug_api/', views.DrugAPIView.as_view(), name='drug_api'),
    path('create/<int:patient_id>/', views.create_treatment, name = 'create_treatment'),
    path('find/', views.find_treatment, name = 'find_treatment'),
    path('', views.home_treatment, name = 'home_treatment'),
    path('diagnosis/', views.home_diagnosis, name = 'home_diagnosis'),
    path('diagnosis/exroom/<int:room_id>/', views.examination_room, name = 'examination_room'),

] 
