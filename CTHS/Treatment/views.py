from datetime import datetime

from django.shortcuts import redirect, render

from User_app.forms import PatientForm

from User_app.models import Patient, Public_Health, Congenital_disease

from Medicine.models import Drug

from rest_framework import status
from rest_framework.views import APIView
from rest_framework.response import Response
from .serializers import Congenital_diseaseSerializer, Congenital_diseaseSerializerWithoutPatient, DrugSerializer

# Create your views here.
def home_patient(request):
    return render(request, 'Treatment/home_patient.html')

def find_patient(request):
    return render(request, 'Treatment/find_patient.html')

def find_treatment(request):
    return render(request, 'Treatment/find_treatment.html')

def create_patient(request):
    if request.method == 'POST':
        form = PatientForm(request.POST)
        if form.is_valid():
            if request.user.id:
                print(request.user.id)
                new_patient = form.save(commit=False)
                creator = Public_Health.objects.get(user_id_id=request.user.id)
                new_patient.public_health_id = creator
                new_patient.save()
                form.save_m2m()
            return redirect('index')
    else:
        form = PatientForm()
    return render(request, 'Treatment/create_patient.html', {'form': form})

def update_patient(request, patient_id):
    context = {}
    patient_data = Patient.objects.get(p_id=patient_id)
    if request.method == 'POST':
        form = PatientForm(request.POST, instance=patient_data)
        context['form'] = form
        if form.is_valid():
            update_data = form.save(commit=False)
            creator = patient_data.public_health_id
            update_data.public_health_id = creator
            update_data.save()
            form.save_m2m()
            context['form'] = PatientForm(instance=update_data)
            context['update'] = True
            context['p_id'] = patient_id
            context['status'] = "อัพเดทข้อมูลเรียบร้อย !"
    else:
        if patient_data:
            context['form'] = PatientForm(instance=patient_data)
            context['update'] = True
            context['p_id'] = patient_id
            return render(request, 'Treatment/create_patient.html', context=context)
        else:
            context['form'] = PatientForm()
            context['update'] = False
    return render(request, 'Treatment/create_patient.html', context=context) 

class Conginetal_diseaseAPIView(APIView):
    """ API โรคประจำตัวของแต่ละ Patient """
    def get(self, request, patient_id):
        patient = Patient.objects.get(p_id=patient_id)
        items = Congenital_disease.objects.filter(patient_id=patient)
        serializer = Congenital_diseaseSerializer(items, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)
    """
    ต้องการเพิ่มโรคประจำตัวจากรายชื่อโรคที่มีอยู่ให้ใช้ post 
    """
    def post(self, request, patient_id):
        print(request.data)
        serializer = Congenital_diseaseSerializer(data=request.data)
        if 'id' in request.data:
            cd_data = Congenital_disease.objects.get(id=request.data['id'])
            cd_data.patient_id.add(request.data['patient_id'])
        if serializer.is_valid():
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    """
    ต้องการเพิ่มโรคประจำตัวใหม่ที่ไม่มีในรายชื่อโรคประจำตัวให้ใช้ patch 
    """
    def patch(self, request, patient_id):
        print(request.data)
        serializer = Congenital_diseaseSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class Conginetal_diseaseWithoutPatientAPIView(APIView):
    """ API โรคประจำตัวทั้งหมด """
    def get(self, request):
        items = Congenital_disease.objects.all()
        serializer = Congenital_diseaseSerializerWithoutPatient(items, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

    def post(self, request):
        serializer = Congenital_diseaseSerializerWithoutPatient(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class DrugAPIView(APIView):
    """ API ยาของแต่ละ Patient """
    def get(self, request, patient_id):
        patient = Patient.objects.get(p_id=patient_id)
        items = Drug.objects.filter(patient=patient)
        serializer = DrugSerializer(items, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)
    """
    ต้องการเพิ่มแพ้ยาจากรายชื่อยาที่มีอยู่
    """
    def post(self, request, patient_id):
        print(request.data)
        serializer = DrugSerializer(data=request.data)
        if 'med_sup_id' in request.data:
            drug_data = Drug.objects.get(med_sup_id=request.data['med_sup_id'])
            drug_data.patient.add(request.data['patient'])
        if serializer.is_valid():
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class DrugWithoutPatientAPIView(APIView):
    """ API ยาทั้งหมด """
    def get(self, request):
        items = Drug.objects.all()
        serializer = DrugSerializer(items, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

def create_treatment(request, patient_id):
    return render(request, 'Treatment/create_treatment.html')

def home_treatment(request):
    return render(request, 'Treatment/home_treatment.html')


def home_diagnosis(request):
    return render(request, 'Treatment/home_diagnosis.html')

def examination_room(request, room_id):
    return render(request, 'Treatment/examination_room.html')
