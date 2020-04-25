from django import forms
from django.forms import ModelForm
from django.forms.widgets import (DateInput, NumberInput, RadioSelect, Select,
                                  Textarea, TextInput,CheckboxInput)
from django.utils.translation import gettext_lazy as _

from Treatment.models import Treatment


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



