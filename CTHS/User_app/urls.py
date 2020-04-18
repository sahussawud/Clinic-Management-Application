from django.urls import path  
from User_app import views
  
urlpatterns = [ 
    path('login/', views.my_login, name = 'my_login'),
    path('logout/', views.my_logout, name = 'my_logout'), 
    path('change_password/', views.ChangePassword, name = 'ChangePassword'), 
    path('create_account/', views.createAccount, name='createAccount'),
    path('', views.homepage , name = 'index'),

] 
