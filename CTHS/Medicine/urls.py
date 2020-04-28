from operator import index

from django.urls import path
from Medicine import views

urlpatterns = [ 
    # path('', views.my_login, name = 'my_login'),

    path('', views.home_medicine, name = 'home_medicine'),
    #จัดการคลังยา มี formmodel
    path('addmedicine/', views.add_medicine, name = 'add_medicine'),
    
    #จอัพเดจคลังยา มี formmodel
    path('updatemedicine/', views.update_medicine, name = 'update_medicine'),
    #ห้องจ่ายยา
    path('comfirmdispensing/', views.comfirm_dispensing, name = 'comfirm_dispensing'),
    # update ข้อมูลยา
    path('updatemedicine/<int:med_sup_id>/', views.update, name = 'update'),

    
    path('prescription/<int:pst_id>/pst_api/', views.PrescriptionAPIView.as_view(), name='pst_api'),

    path('prescription/pst_api/', views.PrescriptionAllWaitAPIView.as_view(), name='pst_api'),

    path('dispense/<int:pst_id>/dispense_api/', views.DispenseAPIView.as_view(), name="dispense_api"),
    
   
] 
