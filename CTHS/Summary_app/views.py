from django.shortcuts import render
from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView
from Treatment.models import Treatment, Symptom
from Treatment.serializers import TreatmentSerializer, SymptomSerializer, SymptomTypeSerializer
from django.db.models import Count
# Create your views here.

def dashboard(request):
    contexts={}
    return render(request, 'Summary_app/dashboard.html', context=contexts)

class ReportAPIView(APIView):
    """
    API ดึงข้อมูลรายงานประวัติการรักษาจากชนิดของอาการและ filter จากวันที่
    """
    def get(self, request):
        symptom_type = request.GET.get('type')
        start_date = request.GET.get('start_date')
        end_date = request.GET.get('end_date')
        items = Symptom.objects.filter(symptom_type=symtom_type, treatment__create_date__gte=start_date, treatment__create_date__lte=end_date)
        serializer = SymptomSerializer(items, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

class ReportTypeAPIView(APIView):
    """
    API ดึงข้อมูลรายงานประวัติการรักษา filter จากวันที่ ของชนิดอาการแต่ละประเภท
    """
    def get(self, request):
        start_date = request.GET.get('start_date')
        end_date = request.GET.get('end_date')
        items = Symptom.objects.filter(treatment__create_date__gte=start_date, treatment__create_date__lte=end_date).values('symptom_type').annotate(p_count=Count('symptom_type'))
        serializer = SymptomTypeSerializer(items, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)