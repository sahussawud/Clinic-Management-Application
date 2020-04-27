from http.client import HTTPResponse
from urllib import request
from django.contrib import messages
from django.shortcuts import redirect, render
from django.views.decorators.csrf import csrf_exempt
from User_app.models import Doctor
from Medicine.models import Drug, Med_supply
from Medicine.forms import MedicineSupplyForm
from Medicine.forms import MedicineDrugForm,UpdateMedForm


from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView
from .serializers import *
# Create your views here.
def add_medicine(request):
    
    if request.method == 'POST':
        form =  MedicineDrugForm(request.POST)
        
        if form.is_valid():
            drug_id = form.cleaned_data['drug_id']
            name = form.cleaned_data['name']
            amount = form.cleaned_data['amount']
            description = form.cleaned_data['description']
            post = Drug(
                drug_id=drug_id,
                name=name,
                amount=amount,
                description=description,

            )
            post.save()
    medicine = MedicineDrugForm()

    return render(request, 'Medicine/add_medicine.html',context={
        'form': medicine,
   
})

    # บันทึก ลง DB
    # if request.method == 'POST':
        
    #     med_id = request.POST.get('med_id')
    #     name = request.POST.get('name')
    #     amount = request.POST.get('amount')
    #     types = request.POST.get('types')
    #     description = request.POST.get('description')
       
    #     if types == 'Drug':
    #         add_med = Drug(
    #             drug_id=med_id,
    #             name=name,
    #             amount=amount,
    #             description=description,
    #         )
    #         add_med.save()
    #     else:
    #         add_med = Med_supply(
    #             sup_id=med_id,
    #             name=name,
    #             amount=amount,
    #             description=description,  
    #         )
    #         add_med.save()     
    # return render(request, 'Medicine/add_medicine.html',context={
    #     'form': medicine,
   
    # })
# --------------------------------
def update_medicine(request):
    return render(request, 'Medicine/update_medicine.html')

    """
    เมื่อกด เลือกยาที่จะ update จะเข้า view
    นี้ละเมื่อทำการบันทึกสำเร็จ จะrender กลับไปหน้า จัดการคลังยา
     """
def update(request):
    if request.method == 'POST':
        form1 =  UpdateMedForm(request.POST)
        if form1.is_valid():
            amount = form1.cleaned_data['amount']
            post = Drug(
                
                amount=amount,
            )
            post.save()
    medicine = UpdateMedForm()

    return render(request,'Medicine/update.html',context={
        'form1': medicine,})

def home_medicine(request):
    return render(request, 'Medicine/home_medicine.html')

def comfirm_dispensing(request):
    return render(request, 'Medicine/comfirm_dispensing.html')

class PrescriptionAPIView(APIView):
    """
    API ดึงข้อมูลใบสั่งยาพร้อมยาที่ต้องจ่าย
    """
    def get(self, request, pst_id):
        pst_data = Prescription.objects.get(id=pst_id)
        serializer = PrescriptionSerializer(pst_data)
        return Response(serializer.data, status=status.HTTP_200_OK)
    """
    API สร้างใบสั่งยา
    DATA REQUIRED:  detail : <string:ข้อมูลรายละเอียดการจ่ายยา>
                    treatment_cn : <int: ID ของประวัติการรักษาที่ต้องการเชื่อมกับใบสั่งยา>
                    doctor_id : <int: ID ของแพทย์ผู้สร้างใบสั่งยา>
    """
    def post(self, request, pst_id):
        serializer = PrescriptionSerializer(data=request.data)
        if serializer.is_valid():
            try:  
                creator = Doctor.objects.get(user_id_id=request.data['doctor_id'])
                serializer.doctor_id = creator
                serializer.save()
            except Doctor.DoesNotExist:
                messages.error(request, ' Doctor.DoesNotExist!')

            
            return Response(serializer.data, status=status.HTTP_201_CREATED)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    """
    API ยืนยันการจ่ายยาพร้อมอัพเดตจำนวนยาหรือเวชภัณฑ์ในคลัง
    DATA REQUIRED: nurse_id : <int: ID ของพยาบาลผู้ยืนยันการจ่ายยา>
    """
    def patch(self, request, pst_id):
        pst_data = Prescription.objects.get(id=pst_id)
        serializer = PrescriptionSerializer(data=request.data, instance=pst_data)
        dispense_data = Dispense.objects.filter(prescription_id=pst_id)
        if serializer.is_valid():
            if pst_data.status == "W":
                for data in dispense_data:
                    if data.type == "D":
                        drug_data = Drug.objects.get(med_sup_id=data.dis_drug_id.med_sup_id)
                        if drug_data.amount >= data.amount:
                            drug_data.amount -= data.amount
                        drug_data.save()
                        
                    elif data.type == "M":
                        med_data = Med_supply.objects.get(med_sup_id=data.dis_med_id.med_sup_id)
                        if med_data.amount >= data.amount:
                            med_data.amount -= data.amount
                        med_data.save()
                
                pst_data.nurse_id = Nurse.objects.get(id=request.data['nurse_id'])
                pst_data.status = "C"
                pst_data.save()
            return Response(serializer.data, status=status.HTTP_200_OK)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class PrescriptionAllWaitAPIView(APIView):
    """
    API ใบสั่งยาทั้งหมดที่ยังไม่ได้จ่ายยา
    """
    def get(self, request):
        pst_data = Prescription.objects.filter(status="W")
        serializer = PrescriptionSerializer(pst_data, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

class DispenseAPIView(APIView):
    """
    API ดึงข้อมูลรายการการจ่ายยาทั้งหมดของแต่ละใบสั่งยา
    """
    def get(self, request, pst_id):
        pst_data = Prescription.objects.get(id=pst_id)
        items = Dispense.objects.filter(prescription_id=pst_id)
        serializer = DispenseSerializer(items, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)
    """
    API สร้างรายการการจ่ายยา
    DATA REQUIRED:  type : <string: "D" ยา or "M" เวชภัณฑ์
                    *drug : <int: ID ของยาที่ต้องการจ่าย>
                    *med_sup : <int: ID ของเวชภัณฑ์ที่ต้องการจ่าย>
                    amount : <int:จำนวนการจ่ายยาหรือเวชภัณฑ์ของรายการนั้นๆ>
    * = ใส่ตาม type ที่กำหนด D = drug, M = med_sup
    """
    def post(self, request, pst_id):
        pst_data = Prescription.objects.get(id=pst_id)
        serializer = DispenseSerializer(data=request.data)
        if serializer.is_valid():
            new_dispense = Dispense.objects.create(prescription_id=pst_data, amount=serializer.validated_data['amount'])
            new_dispense.type = request.data['type']
            if request.data['type'] == "D":
                new_dispense.dis_drug_id = Drug.objects.get(med_sup_id=request.data['drug'])
            elif request.data['type'] == "M":
                new_dispense.dis_med_id = Med_supply.objects.get(med_sup_id=request.data['med_sup'])
            
            new_dispense.save()
            items = Dispense.objects.filter(prescription_id=pst_data)
            serializer = DispenseSerializer(items, many=True)
            return Response(serializer.data, status=status.HTTP_201_CREATED)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)