from datetime import datetime

from django.contrib import messages

from django.contrib.messages.api import success
from django.shortcuts import redirect, render
from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView

from Medicine.models import Drug
from User_app.forms import PatientForm
from User_app.models import Congenital_disease, Patient, Public_Health

from .serializers import (Congenital_diseaseSerializer,
                          Congenital_diseaseSerializerWithoutPatient,
                          DrugSerializer)

from Medicine.models import Drug

from rest_framework import status
from rest_framework.views import APIView
from rest_framework.response import Response
from .serializers import Congenital_diseaseSerializer, Congenital_diseaseSerializerWithoutPatient, DrugSerializer, PatientSerializer
from django.db.models import Q

# Create your views here.
def home_patient(request):
    return render(request, 'Treatment/home_patient.html')

def find_patient(request):
    return render(request, 'Treatment/find_patient.html')

def find_treatment(request):
    return render(request, 'Treatment/find_treatment.html')

def create_patient(request):
    contexts={}
    if request.method == 'POST':
        form = PatientForm(request.POST)
        if form.is_valid():
            if request.user.id:
                new_patient = form.save(commit=False)
                creator = Public_Health.objects.get(user_id_id=request.user.id)
                new_patient.public_health_id = creator
                new_patient.save()
                form.save_m2m()
                messages.success(request, 'โปรไฟล์ผู้ป่วยถูกสร้างสำเร็จ!')
                contexts['patient_id'] =  new_patient.p_id
        else:
            messages.error(request, 'โปรไฟล์ผู้ป่วยถูกสร้างไม่สำเร็จ!')
            form = PatientForm(request.POST)
                 
    else:
        form = PatientForm()

    contexts['form'] = form


    return render(request, 'Treatment/create_patient.html',context=contexts)

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
            context['patient_id'] = patient_id
            context['status'] = "อัพเดทข้อมูลเรียบร้อย !"
    else:
        if patient_data:
            context['form'] = PatientForm(instance=patient_data)
            context['update'] = True
            context['patient_id'] = patient_id
            return render(request, 'Treatment/create_patient.html', context=context)
        else:
            context['form'] = PatientForm()
            context['update'] = False
    return render(request, 'Treatment/create_patient.html', context=context) 

class Conginetal_diseaseAPIView(APIView):
    """ API โรคประจำตัวของแต่ละ Patient 
    25/4/2020 9.38 เเก้ให้ filter เฉพาะ โรคที่ ผป ไม่เป็นอยู่ออกไป
    """
    def get(self, request, patient_id):
        patient = Patient.objects.get(p_id=patient_id)
        print(request.data)
        if 'keywords' in request.GET:
            items = Congenital_disease.objects.exclude(patient_id=patient).filter(name__icontains=request.GET['keywords']).order_by('name')
        else:
            items = Congenital_disease.objects.filter(patient_id=patient).order_by('name')
        serializer = Congenital_diseaseSerializer(items, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)
    """
    ต้องการเพิ่มโรคประจำตัวจากรายชื่อโรคที่มีอยู่ให้ใช้ post 
    DATA REQUIRED:  id : <int: ID ของโรคประจำตัวที่ต้องการเพิ่ม>
                    name : <string: ชื่อของโรคที่ต้องการเพิ่ม>
    *** เพิ่มโรคประจำตัวจากรายชื่อที่มีอยู่ให้กับผู้ป่วยที่ส่งมาพร้อม Path เท่านั้น ***
    """
    def post(self, request, patient_id):
        print(request.data)
        serializer = Congenital_diseaseSerializer(data=request.data)
        patient_data = Patient.objects.get(p_id=patient_id)
        if 'id' in request.data:
            cd_data = Congenital_disease.objects.get(id=request.data['id'])
            cd_data.patient_id.add(patient_data)
        if serializer.is_valid():
            items = Congenital_disease.objects.filter(patient_id=patient_data)
            serializer = Congenital_diseaseSerializer(items, many=True)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    """
    ต้องการเพิ่มโรคประจำตัวใหม่ที่ไม่มีในรายชื่อโรคประจำตัวให้ใช้ patch
    DATA REQUIRED: name : <string: ชื่อของโรคประจำตัวที่ต้องการเพิ่ม>
    *** เพิ่มโรคประจำตัวจากรายชื่อที่มีอยู่ให้กับผู้ป่วยที่ส่งมาพร้อม Path เท่านั้น ***
    """
    def patch(self, request, patient_id):
        print(request.data)
        patient_data = Patient.objects.get(p_id=patient_id)
        serializer = Congenital_diseaseSerializer(data=request.data)
        if serializer.is_valid():
            cd_data = serializer.save()
            cd_data.patient_id.add(patient_data)
            items = Congenital_disease.objects.filter(patient_id=patient_data)
            serializer = Congenital_diseaseSerializer(items, many=True)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    """
    ลบประวัติโรคประจำตัวจากคนไข้
    DATA REQUIRED:  id : <int: ID ของโรคประจำตัวนั้นๆ>
                    name : <string: ชื่อของโรคที่ต้องการลบ>
    *** ลบโรคประจำตัวจากผู้ป่วยที่ส่งมาพร้อม Path เท่านั้น ***
    """
    def delete(self, request, patient_id):
        print(request.data)
        serializer = Congenital_diseaseSerializer(data=request.data)
        patient_data = Patient.objects.get(p_id=patient_id)
        if 'id' in request.data:
            cd_data = Congenital_disease.objects.get(id=request.data['id'])
            cd_data.patient_id.remove(patient_data)
        if serializer.is_valid():
            items = Congenital_disease.objects.filter(patient_id=patient_data)
            serializer = Congenital_diseaseSerializer(items, many=True)
            return Response(serializer.data, status=status.HTTP_200_OK)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class Conginetal_diseaseWithoutPatientAPIView(APIView):
    """ API โรคประจำตัวทั้งหมด
        25/4/2020 9.38 เเก้ให้ filter เฉพาะ โรคที่ ผป ไม่ """
    def get(self, request):
        if 'keywords' in request.GET:
            print(request.GET['keywords'])
            items = Congenital_disease.objects.filter(name__icontains=request.GET['keywords']).order_by('name')
        else:
            items = Congenital_disease.objects.all().order_by('name')
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
        if 'keywords' in request.GET:
            items = Drug.objects.exclude(patient=patient).filter(name__icontains=request.GET['keywords']).order_by('name')
            print(items)
        else:
            items = Drug.objects.filter(patient=patient).order_by('name')
        serializer = DrugSerializer(items, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)
    """
    ต้องการเพิ่มแพ้ยาจากรายชื่อยาที่มีอยู่
    DATA REQUIRED : med_sup_id : <int: ID ของยาจาก model Drug>
    *** สร้างประวัติการแพ้ยาจาก ID Patient ที่ส่งมาพร้อม Path เท่านั้น ***
    """
    def post(self, request, patient_id):
        serializer = DrugSerializer(data=request.data)
        patient_data = Patient.objects.get(p_id=patient_id)
        if 'med_sup_id' in request.data:
            drug_data = Drug.objects.get(med_sup_id=request.data['med_sup_id'])
            drug_data.patient.add(patient_data)
        if serializer.is_valid():
            items = Drug.objects.filter(patient=patient_data).order_by('name')
            serializer = DrugSerializer(items, many=True)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    """
    ลบประวัติแพ้ยาจากคนไข้
    DATA REQUIRED:  med_sup_id : <int: ID ของแพ้ยานั้นๆ>
                    name : <string: ชื่อของยาที่ต้องการลบ>
    *** ลบแพ้ยาจากผู้ป่วยที่ส่งมาพร้อม Path เท่านั้น ***
    """
    def delete(self, request, patient_id):
        print(request.data)
        serializer = DrugSerializer(data=request.data)
        patient_data = Patient.objects.get(p_id=patient_id)
        if 'med_sup_id' in request.data:
            drug_data = Drug.objects.get(med_sup_id=request.data['med_sup_id'])
            drug_data.patient.remove(patient_data)
        if serializer.is_valid():
            items = Drug.objects.filter(patient=patient_data).order_by('name')
            serializer = DrugSerializer(items, many=True)
            return Response(serializer.data, status=status.HTTP_200_OK)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    

'''update api to filter data'''
class DrugWithoutPatientAPIView(APIView):
    """ API ยาทั้งหมด """
    def get(self, request):
        if 'keywords' in request.data:
            items = Drug.objects.filter(name__icontains=request.data['keywords']).order_by('name')
        else:
            items = Drug.objects.all().order_by('name')
        serializer = DrugSerializer(items, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

class PatientSearchAPIView(APIView):
    """ 
    API ค้นหาคนไข้ 
    DATA REQUIRED : search : <string: keyword ที่ต้องการค้นหาจาก ชื่อ - นามสกุล, รหัสบัตรประชาชน, เบอร์โทรศัพท์, หรือ รหัสประจำตัว>
    """
    def get(self, request):
        print(request.data)
        items = Patient.objects.filter(Q(fname__icontains=request.data['search']) | Q(lname__icontains=request.data['search']) | Q(idcard_number__icontains=request.data['search'])
        | Q(phone__icontains=request.data['search']) | Q(id_code__icontains=request.data['search'])).order_by('fname')
        serializer = PatientSerializer(items, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

def create_treatment(request, patient_id):
    return render(request, 'Treatment/create_treatment.html')

def home_treatment(request):
    return render(request, 'Treatment/home_treatment.html')


def home_diagnosis(request):
    return render(request, 'Treatment/home_diagnosis.html')

def examination_room(request, room_id):
    return render(request, 'Treatment/examination_room.html')
