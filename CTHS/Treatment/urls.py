from django.urls import path  
from Treatment import views
  
urlpatterns = [ 
    path('patient/', views.home_patient, name = 'home_patient'),
    path('patient/create/', views.create_patient, name = 'create_patient'),

] 
