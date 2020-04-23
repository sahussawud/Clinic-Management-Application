from django.urls import path  
from Treatment import views
  
urlpatterns = [ 
    path('patient/', views.home_patient, name = 'home_patient'),
    path('patient/find/', views.find_patient, name = 'find_patient'),
    path('patient/create/', views.create_patient, name = 'create_patient'),
    path('create/<int:patient_id>/', views.create_treatment, name = 'create_treatment'),
    path('', views.home_treatment, name = 'home_treatment'),
    path('diagnosis/', views.home_diagnosis, name = 'home_diagnosis'),
    path('diagnosis/exroom/<int:room_id>/', views.examination_room, name = 'examination_room'),

] 
