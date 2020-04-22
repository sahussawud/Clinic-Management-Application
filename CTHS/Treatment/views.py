from django.shortcuts import render

# Create your views here.
def home_patient(request):
    return render(request, 'Treatment/home_patient.html')

def create_patient(request):
    return render(request, 'Treatment/create_patient.html')

def create_treatment(request, patient_id):
    return render(request, 'Treatment/create_treatment.html')

def create_diagnosis(request, treatment_id):
    return render(request, 'Treatment/create_diagnosis.html')