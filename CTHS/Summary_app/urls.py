from django.urls import path  
from Summary_app import views
  
urlpatterns = [ 
    path('', views.dashboard, name = 'dashboard'),

] 
