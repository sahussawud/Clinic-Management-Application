from django.shortcuts import render

# Create your views here.
def home_patient(request):
    return render(request, 'Treatment/home_patient.html')

def create_patient(request):
    if request.method == 'POST':
        firstName = request.POST.get('firstName')
        lastName = request.POST.get('lastName')
        ssid = request.POST.get('ssid')
        dateofbirth = request.POST.get('dateofbirth')
        nation = request.POST.get('nation')
        mature_land = request.POST.get('mature_land')
        patientRole = request.POST.get('patientRole')
        patientStatus = request.POST.get('patientStatus')
        ref_code = request.POST.get('ref_code')
        bloodType = request.POST.get('bloodType')
        address = request.POST.get('address')
        province = request.POST.get('province')
        zip = request.POST.get('zip')
    return render(request, 'Treatment/create_patient.html')

def create_treatment(request, patient_id):
    return render(request, 'Treatment/create_treatment.html')

def create_diagnosis(request, treatment_id):
    return render(request, 'Treatment/create_diagnosis.html')