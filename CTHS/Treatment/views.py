from datetime import date, datetime

from django.contrib import messages
from django.contrib.messages.api import success
from django.core.exceptions import ObjectDoesNotExist
from django.db.models import Q
from django.forms import modelformset_factory
from django.forms.formsets import formset_factory
from django.shortcuts import redirect, render
from django.contrib.auth.decorators import login_required, permission_required
from Treatment.forms import LesionForm
from Medicine.models import Drug
from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView
from Treatment.models import Lesion, Room_Queue
from User_app.forms import PatientForm
from User_app.models import Congenital_disease, Patient, Public_Health

from .forms import *
from .serializers import *


# Create your views here.
@login_required
def home_patient(request):
    return render(request, 'Treatment/home_patient.html')
@login_required
def find_patient(request):
    return render(request, 'Treatment/find_patient.html')
@login_required
def find_treatment(request):
    return render(request, 'Treatment/find_treatment.html')
@login_required
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
@login_required
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
            messages.success(request, 'อัพเดทข้อมูลเรียบร้อย!')
        context['patient_id'] = patient_data.p_id
    else:
        if patient_data:
            context['form'] = PatientForm(instance=patient_data)
            context['patient_id'] = patient_data.p_id
        else:
            context['form'] = PatientForm()
    context['update'] = True       
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
    
class DrugWithoutPatientAPIView(APIView):
    """ API ยาทั้งหมด """
    def get(self, request):
        if request.GET.get('keywords'):
            items = Drug.objects.filter(name__icontains=request.GET.get('keywords')).order_by('name')
        else:
            items = Drug.objects.all().order_by('name')
        serializer = DrugSerializer(items, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)
    
class DrugAndMedSupplyWithoutPatientAPIView(APIView):
    """ API ยาและเวชภัณฑ์ทั้งหมด """
    def get(self, request):
        if request.GET.get('keywords'):
            med_sup = Med_supply.objects.filter(name__icontains=request.GET.get('keywords')).order_by('name')
            drug = Drug.objects.filter(name__icontains=request.GET.get('keywords')).order_by('name')
            data = {
                "drug" : drug,
                "med_sup" : med_sup
            }
        else:
            med_sup = Med_supply.objects.all().order_by('name')
            drug = Drug.objects.all().order_by('name')
            data = {
                "drug" : drug,
                "med_sup" : med_sup
            }
        serializer = DrugMedSupplySerializer(data)
        return Response(serializer.data, status=status.HTTP_200_OK)

class PatientSearchAPIView(APIView):
    """ 
    API ค้นหาคนไข้ 
    DATA REQUIRED : search : <string: keyword ที่ต้องการค้นหาจาก ชื่อ - นามสกุล, รหัสบัตรประชาชน, เบอร์โทรศัพท์, หรือ รหัสประจำตัว>
    """
    def get(self, request):
        if request.GET.get('selected') == 'all' and request.GET.get('keywords'):
            items = Patient.objects.filter(Q(fname__icontains=request.GET.get('keywords')) | Q(lname__icontains=request.GET.get('keywords')) | Q(idcard_number__icontains=request.GET.get('keywords'))
            | Q(phone__icontains=request.GET.get('keywords')) | Q(id_code__icontains=request.GET.get('keywords'))).order_by('fname')
        
        elif request.GET.get('selected') == 'name' and request.GET.get('keywords'):
            items = Patient.objects.filter(Q(fname__icontains=request.GET.get('keywords')) | Q(lname__icontains=request.GET.get('keywords'))).order_by('fname')
        
        elif request.GET.get('selected') == 'ssid' and request.GET.get('keywords'):
            items = Patient.objects.filter(idcard_number__icontains=request.GET.get('keywords'))
        
        elif request.GET.get('selected') == 'phone' and request.GET.get('keywords'):
            items = Patient.objects.filter(phone__icontains=request.GET.get('keywords'))
        
        elif request.GET.get('selected') == 'id_code' and request.GET.get('keywords'):
            items = Patient.objects.filter(id_code__icontains=request.GET.get('keywords'))
        else:
            items = Patient.objects.all()

        serializer = PatientSerializer(items, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

class PatientAPIView(APIView):
    """ 
    API ดึงข้อมูลคนไข้ 
    """
    def get(self, request, patient_id):
        print(request.data)
        items = Patient.objects.get(p_id=patient_id)
        serializer = PatientSerializer(items)
        return Response(serializer.data, status=status.HTTP_200_OK)

@login_required
def create_treatment(request, patient_id):
    
    contexts = {}

    LesionFormSet = modelformset_factory(Lesion, extra=2 , max_num=3, exclude=('wound_symptom',))
    formset = LesionFormSet()

    non_form =  Non_Form_SymptomForm()
    rash_form = Rash_SymptomForm()
    wound_form = Wound_SymptomForm()
    con_wound_form = Con_Wound_SymptomForm()
    eye_form = Eye_SymptomForm()
    fever_form = Fever_SymptomForm()
    diarrhea_form = Diarrhea_SymptomForm()
    pain_form = Pain_SymptomForm()
    if request.method == 'POST':
        
        form = TreatmentForm(request.POST)
        diagnosis_type = request.POST.get("Symptom_option")
        print(diagnosis_type)

        switcher = {
            "non_form": Non_Form_SymptomForm(request.POST),
            "skin": Rash_SymptomForm(request.POST),
            "accident": Wound_SymptomForm(request.POST),
            "con_accident": Con_Wound_SymptomForm(request.POST),
            "eyes": Eye_SymptomForm(request.POST),
            "fever": Fever_SymptomForm(request.POST),
            "diarrhea": Diarrhea_SymptomForm(request.POST),
            "pain": Pain_SymptomForm(request.POST)
        }
        symptom_form = switcher.get(diagnosis_type)
        if form.is_valid():
            print('tm')
            treatment_form = form.save(commit=False)
            try:  
                creator = Public_Health.objects.get(user_id_id=request.user.id)
                patient = Patient.objects.get(p_id=patient_id)
            except Public_Health.ObjectDoesNotExist:
                messages.error(request, ' Public_Health.ObjectDoesNotExist!')
            except Patient.ObjectDoesNotExist:
                messages.error(request, 'ไม่มีโปรไฟล์นี้ในคนไข้นี้ในฐานข้อมูล!')

            treatment_form.user_id = request.user
            treatment_form.patient_p_id = patient
            treatment_form.save()
            if symptom_form.is_valid():
                new_symtom_form = symptom_form.save(commit=False)
                symptom = Symptom.objects.create(treatment_id=treatment_form.cn)
                symptom.symptom_type = diagnosis_type
                symptom.save()
                new_symtom_form.symptom = symptom
                
                new_symtom_form.save()
                #add this treatment to queue
                new_queue = Room_Queue.objects.create(treatment=treatment_form)
                new_queue.status = "WD"
                new_queue.save()
                #if accident form
                if diagnosis_type == 'accident':
                    formset = LesionFormSet(request.POST)
                    if formset.is_valid():
                        instances = formset.save(commit=False)
                        wound_symptom = Wound_Symptom.objects.get(symptom=symptom)
                        for instance in instances:
                            instance.wound_symptom = wound_symptom
                            instance.save()
                            print(instance)
                        messages.success(request, 'รายระเอียดบาดเเผลถูกต้อง!')
                    else:
                        messages.error(request, 'กรอกรายระเอียดบาดเเผลให้ถูกต้อง!')

                messages.success(request, 'บันทึกประวัติเบื้องต้นสำเร็จ!')
                form = TreatmentForm(request.POST)
                non_form = Non_Form_SymptomForm(request.POST)
                skin = Rash_SymptomForm(request.POST)
                accident = Wound_SymptomForm(request.POST)
                con_accident = Con_Wound_SymptomForm(request.POST)
                eyes = Eye_SymptomForm(request.POST)
                fever = Fever_SymptomForm(request.POST)
                diarrhea = Diarrhea_SymptomForm(request.POST)
                pain = Pain_SymptomForm(request.POST)
                return redirect('home_patient')

            else:
                treatment_form.delete()
                messages.error(request, 'บันทึกประวัติเบื้องต้นไม่สำเร็จ!')
                form = TreatmentForm(request.POST)
                non_form = Non_Form_SymptomForm(request.POST)
                skin = Rash_SymptomForm(request.POST)
                accident = Wound_SymptomForm(request.POST)
                con_accident = Con_Wound_SymptomForm(request.POST)
                eyes = Eye_SymptomForm(request.POST)
                fever = Fever_SymptomForm(request.POST)
                diarrhea = Diarrhea_SymptomForm(request.POST)
                pain = Pain_SymptomForm(request.POST)

        else:
            messages.error(request, 'บันทึกประวัติเบื้องต้นไม่สำเร็จ!')
            form = TreatmentForm(request.POST)
                 
    else:
        form = TreatmentForm()
        
        
    patient = Patient.objects.get(p_id=patient_id)
    drug = Drug.objects.filter(patient=patient_id)
    cd = Congenital_disease.objects.filter(patient_id=patient_id)

    contexts['form'] = form
    contexts['spec_form'] = {
        'non_form' : non_form,
        'rash_form' : rash_form,
        'wound_form' : wound_form,
        'con_wound_form' : con_wound_form,
        'eye_form' : eye_form,
        'fever_form' : fever_form,
        'diarrhea_form' : diarrhea_form,
        'pain_form' : Pain_SymptomForm,
    }
        
    
    contexts['patient'] = patient
    contexts['drug'] = drug
    contexts['cd'] = cd
    contexts['age'] = patient.age
    contexts['selected'] = request.POST.get("Symptom_option")
    """FormSet""" 

    contexts['formset'] = formset
    return render(request, 'Treatment/create_treatment.html',context=contexts)
@login_required
def home_treatment(request):
    return render(request, 'Treatment/home_treatment.html')

@login_required
def home_diagnosis(request):
    return render(request, 'Treatment/home_diagnosis.html')
@login_required
def switch_symptom(symptom):
    switcher = {
        "non_form": {
            "model" : Non_Form_Symptom,
            "form" : Non_Form_SymptomForm
        },
        "skin": {
            "model" : Rash_Symptom,
            "form" : Rash_SymptomForm
        },
        "accident": {
            "model" : Wound_Symptom,
            "form" : Wound_SymptomForm
        },
        "con_accident": {
            "model" : Con_Wound_Symptom,
            "form" : Con_Wound_SymptomForm
        },
        "eyes": {
            "model" : Eye_Symptom,
            "form" : Eye_SymptomForm
        },
        "fever": {
            "model" : Fever_Symptom,
            "form" : Fever_SymptomForm
        },
        "diarrhea": {
            "model" : Diarrhea_Symptom,
            "form" : Diarrhea_SymptomForm
        },
        "pain": {
            "model" : Pain_Symptom,
            "form" : Pain_SymptomForm
        },
    }
    return switcher.get(symptom, {
            "model" : Non_Form_Symptom,
            "form" : Non_Form_SymptomForm })
@login_required
def diagnosis_treatment(request, treatment_cn):
    contexts = {}
    contexts['treatment_cn'] = treatment_cn
    print(request.method)
    try:
        treatment = Treatment.objects.get(cn=treatment_cn)
        symptom = Symptom.objects.get(treatment=treatment)
        doctor = Doctor.objects.get(user_id=request.user.id)
        try:
            if request.method == 'GET':
                diagnosis = Diagnosis.objects.get(treatment=treatment)
                form =  DiagnosisForm(instance=diagnosis)
                contexts['complete_diagnosis'] = doctor
                messages.info(request, 'การวินิจฉัยถูกสร้างเเล้ว!')
                try:
                    prescript = Prescription.objects.get(treatment_cn=treatment_cn)
                    contexts['Prescription'] = prescript
                    print('p_scriptionid_',prescript.id)
                except Prescription.DoesNotExist:
                    messages.error(request, 'ยังไม่มีการจ่ายยา!')
                    contexts['Prescription'] = ''
                    print('no_pre')
                    
        except ObjectDoesNotExist:
            if request.method == 'GET':
                form = DiagnosisForm()

        if request.method == 'POST':
            if request.POST.get('_method') == 'patch':
                diagnosis = Diagnosis.objects.get(treatment=treatment)
                form =  DiagnosisForm(request.POST, instance=diagnosis)
                if form.is_valid():
                    form.save()
                    contexts['complete_diagnosis'] = doctor
                    messages.warning(request, 'เเก้ไขการวินิจฉัยสำเร็จสำเร็จ!')
                else:
                    messages.error(request, 'เเก้ไขการวินิจฉัยสำเร็จไม่สำเร็จ!')
                    form =  DiagnosisForm(request.POST)
            else:
                form =  DiagnosisForm(request.POST)
                if form.is_valid():
                    diagnosis_form = form.save(commit=False)
                    diagnosis_form.doctor_id = doctor
                    diagnosis_form.treatment = treatment
                    diagnosis_form.save()
                    # form.save_m2m()
                    update_queue = Room_Queue.objects.get(treatment=treatment)
                    update_queue.status = "WP"
                    update_queue.save()
                    messages.success(request, 'สร้างการวินิจฉัยสำเร็จ!')
                    contexts['complete_diagnosis'] = doctor
                else:
                    messages.error(request, 'สร้างการวินิจฉัยไม่สำเร็จ!')
                    form =  DiagnosisForm(request.POST)
        

            

        
        symptom_model = switch_symptom(symptom.symptom_type).get("model")
        instance_symptom = symptom_model.objects.get(symptom=symptom.id)
        print(instance_symptom)
            
        
        patient = Patient.objects.get(p_id=treatment.patient_p_id.p_id)
        drug = Drug.objects.filter(patient=patient.p_id)
        cd = Congenital_disease.objects.filter(patient_id=patient.p_id)

        treatment_form = TreatmentFormDisplay(instance=treatment)
        symptom_form = switch_symptom(symptom.symptom_type).get("form")
        symptom_form_display = symptom_form(instance=instance_symptom)
        print(symptom_form_display)

        contexts['symptom'] = symptom.symptom_type
        contexts['drug'] = drug
        contexts['cd'] = cd
        contexts['age'] = patient.age
        contexts['patient'] = patient
        contexts['spec_form'] = {
                                'non_form' : symptom_form_display,
                                'rash_form' : symptom_form_display,
                                'wound_form' : symptom_form_display,
                                'con_wound_form' : symptom_form_display,
                                'eye_form' : symptom_form_display,
                                'fever_form' : symptom_form_display,
                                'diarrhea_form' : symptom_form_display,
                                'pain_form' : symptom_form_display
        }
        contexts['form'] = treatment_form
        contexts['diagnosis_form'] = form
    except ObjectDoesNotExist as e:
        messages.error(request, e)
        print(e)

    return render(request, 'Treatment/create_diagnosis.html', context=contexts)
@login_required
def examination_room(request, room_id):
    return render(request, 'Treatment/examination_room.html')



class RoomQueueAPIView(APIView):
    """
    API ดึงข้อมูลคิวที่รอตรวจ
    """
    def get(self, request):
        items = Room_Queue.objects.filter(status="WD")
        serializer = RoomQueueSerializer(items, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK) 

class RoomQueueMedicineAPIView(APIView):
    """
    API ดึงข้อมูลคิวที่รอจ่ายยา
    """
    def get(self, request):
        items = Room_Queue.objects.filter(status="WP")
        serializer = RoomQueueSerializer(items, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK) 