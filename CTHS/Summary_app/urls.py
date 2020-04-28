from django.urls import path  
from Summary_app import views
  
urlpatterns = [ 
    path('', views.dashboard, name = 'dashboard'),
    path('report/api/', views.ReportAPIView.as_view(), name = 'report_api'),
    path('report/type_api/', views.ReportTypeAPIView.as_view(), name = 'report_api'),
    path('report/patient_api/', views.ReportPatientAPIView.as_view(), name = 'report_api'),
] 
