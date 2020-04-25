from django import forms
from django.forms import ModelForm
from django.forms.widgets import (DateInput, RadioSelect, Select, Textarea,
                                  TextInput)
from django.utils.translation import gettext_lazy as _
from Treatment.models import Treatment

class TreatmentForm(ModelForm):
    class Meta:
        models = Treatment
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
            'patient_condition': _('สิทธิการรักษา'),
        }
        widgets = {
            'weight': TextInput(attrs={'class': 'form-control'}),
            'Height': TextInput(attrs={'class': 'form-control'}),
            'bp': TextInput(attrs={'class': 'form-control'}),
            'pr': TextInput(attrs={'class': 'form-control'}),
            'temp': TextInput(attrs={'class': 'form-control'}),
            'rr': TextInput(attrs={'class': 'form-control'}),
            'o2_sat': TextInput(attrs={'class': 'form-control'}),
            'med_cer':TextInput(attrs={'class': 'form-control'}),
            'patient_condition': TextInput(attrs={'class': 'form-control'}),
            
        }