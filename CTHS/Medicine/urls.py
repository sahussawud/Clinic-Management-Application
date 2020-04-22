from django.urls import path  
from Medicine import views
  
urlpatterns = [ 
    # path('', views.my_login, name = 'my_login'),
    path('addmedicine/', views.add_medicine, name = 'add_medicine'),
] 
