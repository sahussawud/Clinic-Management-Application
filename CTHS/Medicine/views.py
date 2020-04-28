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
from Treatment.models import Room_Queue
# Create your views here.


"""
บันทึกยาลงฐานข้อมูล แบบเป็น 2ประเภท ยากับเวชภัณฑ์
ถ้า types == 1 แสดงว่าต้องการเพิ่มยา จะเข้า if เพื่อนำ
    form1 ที่จะนำไปเพิ่มลงdatabase  Drug
ถ้า types == 2 แสดงว่าต้องการเพิ่มเวชภัณฑ์ จะเข้า elie เพื่อนำ
    form2 ที่จะนำไปเพิ่มลงdatabase Med_sup
"""
def home_medicine(request):
    return render(request, 'Medicine/home_medicine.html')

def comfirm_dispensing(request):
    return render(request, 'Medicine/comfirm_dispensing.html')

def add_medicine(request):
    if request.method == 'POST':
        if request.POST.get('types') == '1':
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
                messages.success(request, 'บันทึกข้อมูลเรียบร้อย!')
            else:
                messages.error(request, 'บันทึกข้อมูลไม่สำเร็จ!')
                
        # types = supply
        else:
            form =  MedicineSupplyForm(request.POST)
            if form.is_valid():
                sup_id = form.cleaned_data['sup_id']
                name = form.cleaned_data['name']
                amount = form.cleaned_data['amount']
                description = form.cleaned_data['description']
                post = Med_supply(
                    sup_id=sup_id,
                    name=name,
                    amount=amount,
                    description=description,

                )
                post.save()
                messages.success(request, 'บันทึกข้อมูลเรียบร้อย!')

    medicine = MedicineDrugForm()
    supply = MedicineSupplyForm()
    return render(request, 'Medicine/add_medicine.html',context={
        'form1': medicine,
        'form2': supply, 
})


def update_medicine(request): 
    return render(request, 'Medicine/update_medicine.html')
 
def update(request, med_sup_id):
    """
    เมื่อกด เลือกยาที่จะ update จะเข้า view
    นี้ละเมื่อทำการบันทึกสำเร็จ จะrender กลับไปหน้า จัดการคลังยา

     """
    update_data = Drug.objects.get(med_sup_id=med_sup_id)
    if request.method == 'POST':

        form1 = UpdateMedForm(request.POST)     
        if form1.is_valid():
            update_data.name = request.POST.get('name')
            update_data.amount = request.POST.get('amount')
            update_data.save()
            form1.save
            messages.success(request, 'อัพเดทข้อมูลเรียบร้อย!')
            return render(request, 'Medicine/update_medicine.html')
        else:
            messages.error(request,'บันทึกข้อมูลไม่สำเร็จ!!!!')
    return render(request, 'Medicine/update.html',context={
        'form1': update_data,})

def detail_med(request,med_sup_id):
    data = Drug.objects.get(med_sup_id=med_sup_id)
    form = MedicineDrugForm(request.POST) 
    if form.is_valid():
            data.drug_id = request.POST.get('drug_id')
            data.name = request.POST.get('name')
            data.amount = request.POST.get('amount')
            data.description = request.POST.get('description')
            

    return render(request, 'Medicine/detail_med.html',context={
        'form': data,})

class PrescriptionAPIView(APIView):
    """
    API ดึงข้อมูลใบสั่งยาพร้อมยาที่ต้องจ่าย
    """
    def get(self, request, pst_id):
        pst_data = Prescription.objects.get(id=pst_id)
        serializer = PrescriptionSerializer(pst_data)
        return Response(serializer.data, status=status.HTTP_200_OK)
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
                update_queue = Room_Queue.objects.get(treatment=pst_data.treatment_cn)
                update_queue.delete()
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

    """
    API สร้างใบสั่งยา
    DATA REQUIRED:  detail : <string:ข้อมูลรายละเอียดการจ่ายยา>
                    treatment_cn : <int: ID ของประวัติการรักษาที่ต้องการเชื่อมกับใบสั่งยา>
                    doctor_id : <int: ID ของแพทย์ผู้สร้างใบสั่งยา>
    """
    def post(self, request):
        serializer = CreatePrescriptionSerializer(data=request.data)
        serializer.treatment_cn = request.data['treatment_cn']
        if serializer.is_valid():
            try:  
                creator = Doctor.objects.get(user_id_id=request.data['doctor_id'])
                serializer.doctor_id = creator
                
                serializer.save()
            except Doctor.DoesNotExist:
                messages.error(request, 'Doctor.DoesNotExist!')

            
            return Response(serializer.data, status=status.HTTP_201_CREATED)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

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
                    med_id: <int: ID ของยาหรือเวชภัณฑ์>
                    amount : <int:จำนวนการจ่ายยาหรือเวชภัณฑ์ของรายการนั้นๆ>
    """
    def post(self, request, pst_id):
        pst_data = Prescription.objects.get(id=pst_id)
        serializer = CreateDispenseSerializer(data=request.data)
        if serializer.is_valid():
            new_dispense = Dispense.objects.create(prescription_id=pst_data, amount=serializer.validated_data['amount'])
            new_dispense.type = request.data['type']
            if request.data['type'] == "D":
                new_dispense.dis_drug_id = Drug.objects.get(med_sup_id=request.data['med_id'])
            elif request.data['type'] == "M":
                new_dispense.dis_med_id = Med_supply.objects.get(med_sup_id=request.data['med_id'])
            
            new_dispense.save()
            items = Dispense.objects.filter(prescription_id=pst_data)
            serializer = DispenseSerializer(items, many=True)
            return Response(serializer.data, status=status.HTTP_201_CREATED)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)