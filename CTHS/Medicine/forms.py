
from django import forms
from django.forms import ModelForm
from django.forms.widgets import (Select, Textarea,TextInput)
from Medicine.models import Drug,Med_supply








class  MedicineSupplyForm(forms.ModelForm):
    
    class Meta: 
        model =  Med_supply
        fields = ('sup_id','name','amount','description')
        widgets = {
            'sup_id' : TextInput(attrs={'class': 'form-control form-control-sm'}),
            'name' : TextInput(attrs={'class': 'form-control form-control-sm'}),
            'amount': TextInput(attrs={'class': 'form-control form-control-sm'}),
            'description': Textarea(attrs={'class': 'form-control form-control-sm','rows':'5',}),
        }
        lebels={
            'sup_id': 'รหัสเวชภัณฑ์',
            'name': 'ชื่อยา',
            'amount': 'จำนวน',
            'description': 'รายระเอียด',
        }

class  MedicineDrugForm(forms.ModelForm):
    
    class Meta: 
        model =  Drug
        fields = ('drug_id','name','amount','description')
        widgets = {
            'drug_id' : TextInput(attrs={'class': 'form-control form-control-sm'}),
            'name' : TextInput(attrs={'class': 'form-control form-control-sm'}),
            'amount': TextInput(attrs={'class': 'form-control form-control-sm'}),
            'description': Textarea(attrs={'class': 'form-control form-control-sm','rows':'5',}),
        }
        lebels={
            'drug_id': 'รหัสยา',
            'name': 'ชื่อยา',
            'amount': 'จำนวน',
            'description': 'รายระเอียด',
        }
        
