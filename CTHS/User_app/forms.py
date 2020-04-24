from datetime import datetime
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
            'fname': TextInput(attrs={'class': 'form-control'}),
            'lname': TextInput(attrs={'class': 'form-control'}),
            'idcard_number': TextInput(attrs={'class': 'form-control'}),
            'birth_day': DateInput(attrs={'class': 'form-control', 'type': 'date'}),
            'nationality': Select(attrs={'class': 'custom-select d-block w-100'}),
            'race': Select(attrs={'class': 'custom-select d-block w-100'}),
            'status': RadioSelect(attrs={'class': ''}),
            'blood_type': Select(attrs={'class': 'custom-select d-block w-100'}),
            'phone': TextInput(attrs={'class': 'form-control'}),
            'address': Textarea(attrs={'class': 'form-control','rows':'4'}),
            'patient_role': RadioSelect(attrs={'class': ''}),
            'id_code': TextInput(attrs={'class': 'form-control'}),
            'hospital_refer': TextInput(attrs={'class': 'form-control'}),
            'gold_card_no': TextInput(attrs={'class': 'form-control'}),
            'gold_card_expire': DateInput(attrs={'class': 'form-control', 'type': 'date' }),
        }
    def clean_birth_day(self):
        current_date = datetime.now().date()
        if self.cleaned_data['birth_day'] >= current_date:
            raise forms.ValidationError("วัน/เดือน/ปี เกิดไม่ถูกต้อง !")
        return self.cleaned_data['birth_day']

    def clean_gold_card_expire(self):
        current_date = datetime.now().date()
        if self.cleaned_data['gold_card_expire']:
            if self.cleaned_data['gold_card_expire'] >= current_date:
                raise forms.ValidationError("วันหมดอายุบัตรทองไม่ถูกต้อง !")
        else:
            if "-" in self.cleaned_data['gold_card_no']:
                return self.cleaned_data['gold_card_expire']
            else:
                raise forms.ValidationError("กรุณากรอกวันหมดอายุบัตรทอง !")
        return self.cleaned_data['gold_card_expire']