from datetime import datetime
from django import forms
from django.forms import ModelForm
from django.forms.widgets import (DateInput, RadioSelect, Select, Textarea,
                                  TextInput)
from django.utils.translation import gettext_lazy as _
from User_app.models import Patient

class PatientForm(ModelForm):
    
    class Meta:
        model = Patient
        exclude = ['p_id', 'age', 'public_health_id', 'date']
        labels = {
            'fname': _('ชื่อ'),
            'lname': _('นามสกุล'),
            'idcard_number': _('รหัสบัตรประชาชน'),
            'birth_day': _('วัน/เดือน/ปี เกิด'),
            'race': _('เชื้อชาติ'),
            'nationality': _('สัญชาติ'),
            'status': _('สถานะ'),
            'blood_type': _('กลุ่มเลือด'),
            'phone': _('เบอร์โทรศัพท์'),
            'address': _('ที่อยู่'),
            'patient_role': _('สิทธิการรักษา'),
            'id_code': _('รหัสประจำตัว'),
            'hospital_refer': _('โรงพยาบาลที่ส่งต่อ'),
            'gold_card_no': _('เลขที่บัตรทอง'),
            'gold_card_expire': _('วันหมดอายุบัตรทอง'),
        }
        widgets = {
            'fname': TextInput(attrs={'class': 'form-control', 'v-model':'form[0]', 'v-on:blur':'update'}),
            'lname': TextInput(attrs={'class': 'form-control', 'v-model':'form[1]', 'v-on:blur':'update'}),
            'idcard_number': TextInput(attrs={'class': 'form-control', 'v-model':'form[2]', 'v-on:blur':'update'}),
            'birth_day': DateInput(attrs={'class': 'form-control', 'type': 'date', 'v-model':'form[3]', 'v-on:blur':'update'}),
            'nationality': Select(attrs={'class': 'custom-select d-block w-100', 'v-model':'form[4]', 'v-on:blur':'update'}),
            'race': Select(attrs={'class': 'custom-select d-block w-100', 'v-model':'form[5]', 'v-on:blur':'update'}),
            'status': RadioSelect(attrs={'class': '', 'v-model':'form[6]', 'v-on:blur':'update'}),
            'blood_type': Select(attrs={'class': 'custom-select d-block w-100', 'v-model':'form[7]', 'v-on:blur':'update'}),
            'phone': TextInput(attrs={'class': 'form-control', 'v-model':'form[8]', 'v-on:blur':'update'}),
            'address': Textarea(attrs={'class': 'form-control','rows':'4', 'v-model':'form[9]', 'v-on:blur':'update'}),
            'patient_role': RadioSelect(attrs={'class': '', 'v-model':'form[10]', 'v-on:blur':'update'}),
            'id_code': TextInput(attrs={'class': 'form-control', 'v-model':'form[11]', 'v-on:blur':'update'}),
            'hospital_refer': TextInput(attrs={'class': 'form-control', 'v-model':'form[12]', 'v-on:blur':'update'}),
            'gold_card_no': TextInput(attrs={'class': 'form-control', 'v-model':'form[13]', 'v-on:blur':'update'}),
            'gold_card_expire': DateInput(attrs={'class': 'form-control', 'type': 'date' , 'v-model':'form[14]', 'v-on:blur':'update'}),
        }
    def clean_birth_day(self):
        current_date = datetime.now().date()
        if self.cleaned_data['birth_day'] >= current_date:
            raise forms.ValidationError("วัน/เดือน/ปี เกิดไม่ถูกต้อง !")
        return self.cleaned_data['birth_day']

    def clean_gold_card_expire(self):
        current_date = datetime.now().date()
        if self.cleaned_data['gold_card_expire']:
            if self.cleaned_data['gold_card_expire'] < current_date:
                raise forms.ValidationError("วันหมดอายุบัตรทองไม่ถูกต้อง !")
        else:
            if "" in self.cleaned_data['gold_card_no']:
                return self.cleaned_data['gold_card_expire']
            else:
                raise forms.ValidationError("กรุณากรอกวันหมดอายุบัตรทอง !")
        return self.cleaned_data['gold_card_expire']

    def clean_id_code(self):
        try:
            Patient.objects.get(id_code=self.cleaned_data['id_code'])
            raise forms.ValidationError("รหัสประจำตัวนี้ เคยลงทะเบียนเเล้ว !")
        except Patient.DoesNotExist:
            return self.cleaned_data['id_code']