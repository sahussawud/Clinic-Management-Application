from django.shortcuts import render

# Create your views here.
def add_medicine(request):
    return render(request, 'Medicine/add_medicine.html')
def update_medicine(request):
    return render(request, 'Medicine/update_medicine.html')
