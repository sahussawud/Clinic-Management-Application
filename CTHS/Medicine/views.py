from http.client import HTTPResponse
from urllib import request

from django.shortcuts import render
from django.views.decorators.csrf import csrf_exempt
from Medicine.models import Drug,Med_supply


# Create your views here.
def add_medicine(request):
    if request.method == 'POST':
        
        med_sup_id = request.POST.get('med_sup_id')
        name = request.POST.get('name')
        amount = request.POST.get('amount')
        types = request.POST.get('types')
        if types == 'Drug':
            add_med = Drug(
                med_sup_id=med_sup_id,
                name=name,
                amount=amount,
            )
            add_med.save()
        else:
            add_med = Med_supply(
                med_sup_id=med_sup_id,
                name=name,
                amount=amount,
                
            )
            add_med.save()
        
        
    return render(request, 'Medicine/add_medicine.html')

def update_medicine(request):
    return render(request, 'Medicine/update_medicine.html')

def home_medicine(request):
    return render(request, 'Medicine/home_medicine.html')

def comfirm_dispensing(request):
    return render(request, 'Medicine/comfirm_dispensing.html')



    

