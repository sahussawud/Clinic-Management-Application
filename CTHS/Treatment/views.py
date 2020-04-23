from django.shortcuts import redirect, render

from User_app.models import PatientForm, Public_Health


# Create your views here.
def home_patient(request):
    return render(request, 'Treatment/home_patient.html')

def create_patient(request):
    if request.method == 'POST':
        form = PatientForm(request.POST)
        if form.is_valid():
            print(form.cleaned_data)
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

def create_treatment(request, patient_id):
    return render(request, 'Treatment/create_treatment.html')

def create_diagnosis(request, treatment_id):
    return render(request, 'Treatment/create_diagnosis.html')
