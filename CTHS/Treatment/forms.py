from django import forms
from django.forms import ModelForm
from django.forms.widgets import (CheckboxInput, DateInput, NumberInput,
                                  RadioSelect, Select, Textarea, TextInput)
from django.utils.translation import gettext_lazy as _

from Treatment.models import *


class TreatmentForm(ModelForm):
    class Meta:
        model = Treatment
        exclude = ['cn', 'create_date', 'user_id', 'patient_p_id']
        labels = {
            'weight': _('น้ำหนัก'),
            'Height': _('ส่วนสูง'),
            'bp': _('ความดันโลหิต'),
            'pr': _('อัตราชีพจร'),
            'temp': _('อุณหภูมิร่างกาย'),
            'rr': _('อัตราการหายใจ'),
            'o2_sat': _('ออกซิเจนในเลือด'),
            'med_cer': _('ใบรับรองเเพทย์'),
            'patient_condition': _('สภาพผู้ป่วย'),
        }
        widgets = {
            'weight': NumberInput(attrs={'class': 'form-control', 'placeholder':'Kilograms'}),
            'Height': NumberInput(attrs={'class': 'form-control', 'placeholder':'Centimetre'}),
            'bp': NumberInput(attrs={'class': 'form-control', 'placeholder':'mmHg'}),
            'pr': NumberInput(attrs={'class': 'form-control', 'placeholder':'BPM'}),
            'temp': NumberInput(attrs={'class': 'form-control', 'placeholder':'Celcuis'}),
            'rr': NumberInput(attrs={'class': 'form-control', 'placeholder':'RPM'}),
            'o2_sat': NumberInput(attrs={'class': 'form-control', 'placeholder':'%'}),
            'med_cer': CheckboxInput(attrs={'class': ''}),
            'patient_condition': RadioSelect(attrs={'class': 'form-check-input'}),
        }

class SymptomForm(ModelForm):
    class Meta:
        model = Symptom
        exclude = ['treatment']

class Icd_10Form(ModelForm):
    class Meta:
        model = Icd_10
        fields = '__all__'

class DiagnosisForm(ModelForm):
    class Meta:
        model = Diagnosis
        exclude = ['Treatment', 'doctor_id','icd_10']

class Non_Form_SymptomForm(ModelForm):
    class Meta:
        model = Non_Form_Symptom
        exclude = ['symptom']

class Rash_SymptomForm(ModelForm):
    class Meta:
        model = Rash_Symptom
        exclude = ['symptom']

class Wound_SymptomForm(ModelForm):
    class Meta:
        model = Wound_Symptom
        exclude = ['symptom']

class LesionForm(ModelForm):
    class Meta:
        model = Lesion
        exclude = ['wound_symptom']
        widgets = {
            'lesion_type' : Select(attrs={'class': 'custom-select'}),
            'lesion_area' : TextInput(attrs={'class': 'form-control'}),
            'lesion_x': TextInput(attrs={'class': 'form-control col-md-4'}),
            'lesion_y': TextInput(attrs={'class': 'form-control col-md-4'}),
        }


    

class Con_Wound_SymptomForm(ModelForm):
    class Meta:
        model = Con_Wound_Symptom
        exclude = ['symptom']

class Eye_SymptomForm(ModelForm):
    class Meta:
        model = Eye_Symptom
        exclude = ['symptom']

class Fever_SymptomForm(ModelForm):
    class Meta:
        model = Fever_Symptom
        exclude = ['symptom']

class Diarrhea_SymptomForm(ModelForm):
    class Meta:
        model = Diarrhea_Symptom
        exclude = ['symptom']

class Pain_SymptomForm(ModelForm):
    class Meta:
        model = Pain_Symptom
        exclude = ['symptom']


