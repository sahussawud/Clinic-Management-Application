from django.urls import path  
from Treatment import views
  
urlpatterns = [ 
    path('/patient', views.home_patient, name = 'home_patient'),

] 
