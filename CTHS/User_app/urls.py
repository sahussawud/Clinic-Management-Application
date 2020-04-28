from django.urls import path  
from User_app import views
  
urlpatterns = [ 
    path('login/', views.my_login, name = 'my_login'),
    path('logout/', views.my_logout, name = 'my_logout'), 
    path('change_password/', views.ChangePassword, name = 'ChangePassword'), 
    path('create_account/', views.createAccount, name='createAccount'),
    path('', views.homepage , name = 'index'),

    path('admin/home/', views.home_admin , name = 'home_admin'),
    path('admin/User_app/user/add/', views.add_user, name='add_user'),
    path('admin/User_app/user/', views.view_user, name='view_user'),

    path('admin/User_app/doctor/add/', views.add_doctor, name='add_doctor'),
    path('admin/User_app/nurse/add/', views.add_nurse, name='add_nurse'),
    path('admin/User_app/public_health/add/', views.add_public_health, name='add_public_health'),

] 
