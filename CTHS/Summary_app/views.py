from django.shortcuts import render

# Create your views here.

def dashboard(request):
    contexts={}
    return render(request, 'Summary_app/dashboard.html', context=contexts)