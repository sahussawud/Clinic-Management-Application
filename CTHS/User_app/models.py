from datetime import datetime

from django.conf import settings
from django.contrib.auth.models import AbstractUser, User
from django import forms
from django.db import models
from django.forms import ModelForm
from django.forms.widgets import (DateInput, RadioSelect, Select, Textarea,
                                  TextInput)
from django.utils.translation import gettext_lazy as _

# Create your models here.

NATIONALITIES_CHOICE = [('Afghan', 'Afghan'), ('Albanian', 'Albanian'), ('Algerian', 'Algerian'), 
                     ('American', 'American'), ('Andorran', 'Andorran'), ('Angolan', 'Angolan'), 
                     ('Antiguans', 'Antiguans'), ('Argentinean', 'Argentinean'), ('Armenian', 'Armenian'), 
                     ('Australian', 'Australian'), ('Austrian', 'Austrian'), ('Azerbaijani', 'Azerbaijani'), 
                     ('Bahamian', 'Bahamian'), ('Bahraini', 'Bahraini'), ('Bangladeshi', 'Bangladeshi'), 
                     ('Barbadian', 'Barbadian'), ('Barbudans', 'Barbudans'), ('Batswana', 'Batswana'), 
                     ('Belarusian', 'Belarusian'), ('Belgian', 'Belgian'), ('Belizean', 'Belizean'), 
                     ('Beninese', 'Beninese'), ('Bhutanese', 'Bhutanese'), ('Bolivian', 'Bolivian'), 
                     ('Bosnian', 'Bosnian'), ('Brazilian', 'Brazilian'), ('British', 'British'), 
                     ('Bruneian', 'Bruneian'), ('Bulgarian', 'Bulgarian'), ('Burkinabe', 'Burkinabe'), 
                     ('Burmese', 'Burmese'), ('Burundian', 'Burundian'), ('Cambodian', 'Cambodian'), 
                     ('Cameroonian', 'Cameroonian'), ('Canadian', 'Canadian'), ('Cape Verdean', 'Cape Verdean'), 
                     ('Central African', 'Central African'), ('Chadian', 'Chadian'), ('Chilean', 'Chilean'), 
                     ('Chinese', 'Chinese'), ('Colombian', 'Colombian'), ('Comoran', 'Comoran'), 
                     ('Congolese', 'Congolese'), ('Costa Rican', 'Costa Rican'), ('Croatian', 'Croatian'), 
                     ('Cuban', 'Cuban'), ('Cypriot', 'Cypriot'), ('Czech', 'Czech'), ('Danish', 'Danish'), 
                     ('Djibouti', 'Djibouti'), ('Dominican', 'Dominican'), ('Dutch', 'Dutch'), 
                     ('Dutchman', 'Dutchman'), ('Dutchwoman', 'Dutchwoman'), ('East Timorese', 'East Timorese'), 
                     ('Ecuadorean', 'Ecuadorean'), ('Egyptian', 'Egyptian'), ('Emirian', 'Emirian'), 
                     ('Equatorial Guinean', 'Equatorial Guinean'), ('Eritrean', 'Eritrean'), 
                     ('Estonian', 'Estonian'), ('Ethiopian', 'Ethiopian'), ('Fijian', 'Fijian'), 
                     ('Filipino', 'Filipino'), ('Finnish', 'Finnish'), ('French', 'French'), 
                     ('Gabonese', 'Gabonese'), ('Gambian', 'Gambian'), ('Georgian', 'Georgian'), 
                     ('German', 'German'), ('Ghanaian', 'Ghanaian'), ('Greek', 'Greek'), 
                     ('Grenadian', 'Grenadian'), ('Guatemalan', 'Guatemalan'), ('Guinea-Bissauan', 'Guinea-Bissauan'), 
                     ('Guinean', 'Guinean'), ('Guyanese', 'Guyanese'), ('Haitian', 'Haitian'), 
                     ('Herzegovinian', 'Herzegovinian'), ('Honduran', 'Honduran'), ('Hungarian', 'Hungarian'), 
                     ('I-Kiribati', 'I-Kiribati'), ('Icelander', 'Icelander'), ('Indian', 'Indian'), 
                     ('Indonesian', 'Indonesian'), ('Iranian', 'Iranian'), ('Iraqi', 'Iraqi'), ('Irish', 'Irish'), 
                     ('Israeli', 'Israeli'), ('Italian', 'Italian'), ('Ivorian', 'Ivorian'), ('Jamaican', 'Jamaican'), 
                     ('Japanese', 'Japanese'), ('Jordanian', 'Jordanian'), ('Kazakhstani', 'Kazakhstani'), 
                     ('Kenyan', 'Kenyan'), ('Kittian and Nevisian', 'Kittian and Nevisian'), ('Kuwaiti', 'Kuwaiti'), 
                     ('Kyrgyz', 'Kyrgyz'), ('Laotian', 'Laotian'), ('Latvian', 'Latvian'), ('Lebanese', 'Lebanese'), 
                     ('Liberian', 'Liberian'), ('Libyan', 'Libyan'), ('Liechtensteiner', 'Liechtensteiner'), 
                     ('Lithuanian', 'Lithuanian'), ('Luxembourger', 'Luxembourger'), ('Macedonian', 'Macedonian'), 
                     ('Malagasy', 'Malagasy'), ('Malawian', 'Malawian'), ('Malaysian', 'Malaysian'), 
                     ('Maldivan', 'Maldivan'), ('Malian', 'Malian'), ('Maltese', 'Maltese'), 
                     ('Marshallese', 'Marshallese'), ('Mauritanian', 'Mauritanian'), ('Mauritian', 'Mauritian'), 
                     ('Mexican', 'Mexican'), ('Micronesian', 'Micronesian'), ('Moldovan', 'Moldovan'), 
                     ('Monacan', 'Monacan'), ('Mongolian', 'Mongolian'), ('Moroccan', 'Moroccan'), 
                     ('Mosotho', 'Mosotho'), ('Motswana', 'Motswana'), ('Mozambican', 'Mozambican'), 
                     ('Namibian', 'Namibian'), ('Nauruan', 'Nauruan'), ('Nepalese', 'Nepalese'), 
                     ('Netherlander', 'Netherlander'), ('New Zealander', 'New Zealander'), ('Ni-Vanuatu', 'Ni-Vanuatu'), 
                     ('Nicaraguan', 'Nicaraguan'), ('Nigerian', 'Nigerian'), ('Nigerien', 'Nigerien'), 
                     ('North Korean', 'North Korean'), ('Northern Irish', 'Northern Irish'), ('Norwegian', 'Norwegian'), 
                     ('Omani', 'Omani'), ('Pakistani', 'Pakistani'), ('Palauan', 'Palauan'), ('Panamanian', 'Panamanian'), 
                     ('Papua New Guinean', 'Papua New Guinean'), ('Paraguayan', 'Paraguayan'), ('Peruvian', 'Peruvian'), 
                     ('Polish', 'Polish'), ('Portuguese', 'Portuguese'), ('Qatari', 'Qatari'), ('Romanian', 'Romanian'), 
                     ('Russian', 'Russian'), ('Rwandan', 'Rwandan'), ('Saint Lucian', 'Saint Lucian'), ('Salvadoran', 'Salvadoran'), 
                     ('Samoan', 'Samoan'), ('San Marinese', 'San Marinese'), ('Sao Tomean', 'Sao Tomean'), ('Saudi', 'Saudi'), 
                     ('Scottish', 'Scottish'), ('Senegalese', 'Senegalese'), ('Serbian', 'Serbian'), ('Seychellois', 'Seychellois'), 
                     ('Sierra Leonean', 'Sierra Leonean'), ('Singaporean', 'Singaporean'), ('Slovakian', 'Slovakian'), 
                     ('Slovenian', 'Slovenian'), ('Solomon Islander', 'Solomon Islander'), ('Somali', 'Somali'), 
                     ('South African', 'South African'), ('South Korean', 'South Korean'), ('Spanish', 'Spanish'), 
                     ('Sri Lankan', 'Sri Lankan'), ('Sudanese', 'Sudanese'), ('Surinamer', 'Surinamer'), ('Swazi', 'Swazi'), 
                     ('Swedish', 'Swedish'), ('Swiss', 'Swiss'), ('Syrian', 'Syrian'), ('Taiwanese', 'Taiwanese'), 
                     ('Tajik', 'Tajik'), ('Tanzanian', 'Tanzanian'), ('Thai', 'Thai'), ('Togolese', 'Togolese'), 
                     ('Tongan', 'Tongan'), ('Trinidadian or Tobagonian', 'Trinidadian or Tobagonian'), ('Tunisian', 'Tunisian'), 
                     ('Turkish', 'Turkish'), ('Tuvaluan', 'Tuvaluan'), ('Ugandan', 'Ugandan'), ('Ukrainian', 'Ukrainian'), 
                     ('Uruguayan', 'Uruguayan'), ('Uzbekistani', 'Uzbekistani'), ('Venezuelan', 'Venezuelan'), 
                     ('Vietnamese', 'Vietnamese'), ('Welsh', 'Welsh'), ('Yemenite', 'Yemenite'), ('Zambian', 'Zambian'), 
                     ('Zimbabwean', 'Zimbabwean')]

class User(AbstractUser):
    phone = models.CharField(_("Phone numbers"), max_length=10)
    address = models.TextField(_("Address"))
    image_url = models.ImageField(upload_to="")
    idcard_number = models.CharField(_("ID card number"), max_length=13)
    nationality = models.CharField(_("Nationality"), max_length=25, default="", choices=NATIONALITIES_CHOICE)
    race = models.CharField(_("Race"), max_length=25, default="", choices=NATIONALITIES_CHOICE)

class Nurse(models.Model):
    user_id = models.OneToOneField(settings.AUTH_USER_MODEL, verbose_name=_("User"), on_delete=models.CASCADE)
    department = models.CharField(_("Department"), max_length=255)

class Doctor(models.Model):
    user_id = models.OneToOneField(settings.AUTH_USER_MODEL, verbose_name=_("User"), on_delete=models.CASCADE)
    specialized_branches = models.CharField(_("Specialized branches (Keen on)"), max_length=255)

class Public_Health(models.Model):
    user_id = models.OneToOneField(settings.AUTH_USER_MODEL, verbose_name=_("User"), on_delete=models.CASCADE)

class Patient(models.Model):
    p_id = models.AutoField(_("Patient ID"), primary_key=True)
    fname = models.CharField(_("Firstname"), max_length=255)
    lname = models.CharField(_("Lastname"), max_length=255)
    idcard_number = models.CharField(_("ID card number"), max_length=13, default="")
    age = models.IntegerField(_("Age"))
    birth_day = models.DateField(_("Birth date"), auto_now=False, auto_now_add=False)
    nationality = models.CharField(_("Nationality"), max_length=25, default="", choices=NATIONALITIES_CHOICE)
    race = models.CharField(_("Race"), max_length=25, default="", choices=NATIONALITIES_CHOICE)
    PATIENT_STATUS_CHOICE = [
        ('S', 'โสด'),
        ('M', 'สมรส'),
        ('O', 'อื่นๆ')
    ]
    status = models.CharField(_("Patient Condition"), max_length=1, choices=PATIENT_STATUS_CHOICE)
    PATIENT_BLOOD_TYPE_CHOICE = [
        ('A', 'A'),
        ('B', 'B'),
        ('O', 'O'),
        ('AB', 'AB')
    ]
    blood_type = models.CharField(_("Blood Type"), max_length=2, choices=PATIENT_BLOOD_TYPE_CHOICE)
    phone = models.CharField(_("Phone"), max_length=10)
    address = models.TextField(_("Address"))
    public_health_id = models.ForeignKey(Public_Health, verbose_name=_("Creator ID"), on_delete=models.DO_NOTHING)
    date = models.DateField(_("Created Date"), auto_now=True)
    PATIENT_ROLE_CHOICE = [
        ('1', 'นักศึกษา'),
        ('2', 'พนักงานเงินงบประมาณ'),
        ('3', 'ข้าราชการ'),
        ('4', 'พนักงานเงินได้'),
        ('5', 'ประกันสังคม'),
        ('6', 'พนักงานพิเศษ'),
        ('7', 'พนักงานเปลี่ยนสภาพ'),
        ('8', 'อื่นๆ')
    ]
    patient_role = models.CharField(_("Patient Role"), max_length=2, choices=PATIENT_ROLE_CHOICE, default='1')
    id_code = models.CharField(_("Personnal ID"), max_length=10, default="", null=True, unique=True)
    hospital_refer = models.CharField(_('Hospital Refer'), max_length=255, default="")
    gold_card_no = models.CharField(_('Gold card no.'), max_length=10, default="")
    gold_card_expire = models.DateField(_("Gold card expire date"), auto_now=False, auto_now_add=False, null=True)


    def age(self):
        return int((datetime.date.today() - self.birth_day).days / 365.25 )
    age = property(age)

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
            'status': Select(attrs={'class': 'custom-select d-block w-100'}),
            'blood_type': Select(attrs={'class': 'custom-select d-block w-100'}),
            'phone': TextInput(attrs={'class': 'form-control'}),
            'address': Textarea(attrs={'class': 'form-control'}),
            'patient_role': RadioSelect(attrs={'class': 'custom-control custom-radio'}),
            'id_code': TextInput(attrs={'class': 'form-control'}),
            'hospital_refer': TextInput(attrs={'class': 'form-control'}),
            'gold_card_no': TextInput(attrs={'class': 'form-control'}),
            'gold_card_expire': DateInput(attrs={'class': 'form-control', 'type': 'date'}),
        }
    def clean_birth_day(self):
        current_date = datetime.now().date()
        if self.cleaned_data['birth_day'] >= current_date:
            raise forms.ValidationError("วัน/เดือน/ปี เกิดไม่ถูกต้อง !")
        return self.cleaned_data['birth_day']

class Congenital_disease(models.Model):
    name = models.CharField(_("Congenital disease name"), max_length=255)
    patient_id = models.ManyToManyField(Patient, verbose_name=_("Patient ID"))
