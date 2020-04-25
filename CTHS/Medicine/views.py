from http.client import HTTPResponse
from urllib import request

from django.shortcuts import redirect, render
from django.views.decorators.csrf import csrf_exempt

from Medicine.models import Drug, Med_supply
from Medicine.forms import MedicineSupplyForm
from Medicine.forms import MedicineDrugForm

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

def home_medicine(request):
    return render(request, 'Medicine/home_medicine.html')

def comfirm_dispensing(request):
    return render(request, 'Medicine/comfirm_dispensing.html')
