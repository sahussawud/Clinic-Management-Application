import datetime

from django.conf import settings
from django.contrib.auth.models import AbstractUser, User
from django.db import models
from django.forms import ModelForm
from django.forms.widgets import Select, Textarea, TextInput
from django.utils.translation import gettext_lazy as _

# Create your models here.

class User(AbstractUser):
    phone = models.CharField(_("Phone numbers"), max_length=10)
    address = models.TextField(_("Address"))
    image_url = models.ImageField(upload_to="")
    idcard_number = models.CharField(_("ID card number"), max_length=13)
    race = models.CharField(_("Race"), max_length=255)
    nationality = models.CharField(_("Nationality"), max_length=255)

class Nurse(models.Model):
    user_id = models.OneToOneField(settings.AUTH_USER_MODEL, verbose_name=_("User"), on_delete=models.CASCADE)
    department = models.CharField(_("Department"), max_length=255)

class Doctor(models.Model):
    user_id = models.OneToOneField(settings.AUTH_USER_MODEL, verbose_name=_("User"), on_delete=models.CASCADE)
    specialized_branches = models.CharField(_("Specialized branches (Keen on)"), max_length=255)

class Public_Health(models.Model):
    user_id = models.OneToOneField(settings.AUTH_USER_MODEL, verbose_name=_("User"), on_delete=models.CASCADE)

class Patient(models.Model):
    p_id = models.CharField(_("Patient ID"), max_length=6, primary_key=True)
    fname = models.CharField(_("Firstname"), max_length=255)
    lname = models.CharField(_("Lastname"), max_length=255)
    idcard_number = models.CharField(_("ID card number"), max_length=13, default="")
    age = models.IntegerField(_("Age"))
    birth_day = models.DateField(_("Birth date"), auto_now=False, auto_now_add=False)
    nationality = models.CharField(_("Nationality"), max_length=255, default="")
    race = models.CharField(_("Race"), max_length=255, default="")
    PATIENT_STATUS_CHOICE = [
        ('S', 'Single'),
        ('M', 'Married'),
        ('O', 'Others')
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
        ('1', 'Student'),
        ('2', 'Budgetary Staff'),
        ('3', 'Official Staff'),
        ('4', 'Employee'),
        ('5', 'Social Security'),
        ('6', 'Special Staff'),
        ('7', 'Changed Employee'),
        ('8', 'Others')
    ]
    patient_role = models.CharField(_("Patient Role"), max_length=2, choices=PATIENT_ROLE_CHOICE, default='1')
    id_code = models.CharField(_("Personnal ID"), max_length=10, default="", null=True, unique=True)

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
        }
        widgets = {
            'fname': TextInput(attrs={'class': 'form-control'}),
            'lname': TextInput(attrs={'class': 'form-control'}),
            'idcard_number': TextInput(attrs={'class': 'form-control'}),
            'birth_day': TextInput(attrs={'class': 'form-control'}),
            'nationality': TextInput(attrs={'class': 'form-control'}),
            'race': TextInput(attrs={'class': 'form-control'}),
            'status': Select(attrs={'class': 'custom-select d-block w-100'}),
            'blood_type': Select(attrs={'class': 'custom-select d-block w-100'}),
            'phone': TextInput(attrs={'class': 'form-control'}),
            'address': Textarea(attrs={'class': 'form-control'}),
            'patient_role': Select(attrs={'class': 'form-control'}),
            'id_code': TextInput(attrs={'class': 'form-control'}),
        }

class Congenital_disease(models.Model):
    name = models.CharField(_("Congenital disease name"), max_length=255)
    patient_id = models.ManyToManyField(Patient, verbose_name=_("Patient ID"))
