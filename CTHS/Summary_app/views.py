from django.shortcuts import render
from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView
from User_app.models import Patient
from Treatment.models import Treatment, Symptom
from Treatment.serializers import TreatmentSerializer, SymptomSerializer, SymptomTypeSerializer, PatientSerializer
from django.db.models import Count
from django.contrib.auth.decorators import login_required, permission_required

# Create your views here.
@login_required
def dashboard(request):
    contexts={}
    return render(request, 'Summary_app/dashboard.html', context=contexts)

class ReportAPIView(APIView):
    """
    API ดึงข้อมูลรายงานประวัติการรักษาจากชนิดของอาการและ filter จากวันที่
    """
    def get(self, request):
        symptom_type = request.GET.get('symptom_type')
        start_date = request.GET.get('start_date')
        end_date = request.GET.get('end_date')
        if symptom_type:
            items = Symptom.objects.filter(symptom_type=symptom_type)
        elif start_date and end_date:
            items = Symptom.objects.filter(treatment__create_date__gte=start_date, treatment__create_date__lte=end_date)
        elif symptom_type and start_date and end_date:
            items = Symptom.objects.filter(symptom_type=symptom_type, treatment__create_date__gte=start_date, treatment__create_date__lte=end_date)
        else:
            items = Symptom.objects.all()

        serializer = SymptomSerializer(items, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

class ReportTypeAPIView(APIView):
    """
    API ดึงข้อมูลรายงานประวัติการรักษา filter จากวันที่ ของชนิดอาการแต่ละประเภท
    """
    def get(self, request):
        if request.GET.get('start_date') and request.GET.get('end_date'):
            start_date = request.GET.get('start_date')
            end_date = request.GET.get('end_date')
            items = Symptom.objects.filter(treatment__create_date__gte=start_date, treatment__create_date__lte=end_date).values('symptom_type').annotate(p_count=Count('symptom_type'))
        else:
            items = Symptom.objects.all().values('symptom_type').annotate(p_count=Count('symptom_type'))
        serializer = SymptomTypeSerializer(items, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

class ReportPatientAPIView(APIView):
    """
    API ดึงข้อมูลรายงานจำนวนผู้ป่วย จากวันที่
    """
    def get(self, request):
        start_date = request.GET.get('start_date')
        end_date = request.GET.get('end_date')
        items = Patient.objects.filter(date__gte=start_date, date__lte=end_date)
        serializer = PatientSerializer(items, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)