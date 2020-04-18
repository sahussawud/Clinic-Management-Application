from django.contrib.auth.models import User
from django.db import models
from django.utils.translation import gettext_lazy as _
from django.contrib.auth.models import AbstractUser
from django.conf import settings
import datetime
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
    age = models.IntegerField(_("Age"))
    birth_day = models.DateField(_("Birth date"), auto_now=False, auto_now_add=False)
    PATIENT_STATUS_CHOICE = [
        ('S', 'Single'),
        ('M', 'Married')
    ]
    status = models.CharField(_("Patient Condition"), max_length=1, choices=PATIENT_STATUS_CHOICE)
    PATIENT_BLOOD_TYPE_CHOICE = [
        ('A', 'A'),
        ('B', 'B'),
        ('O', 'O'),
        ('AB', 'AB')
    ]
    blood_type = models.CharField(_("Patient Condition"), max_length=2, choices=PATIENT_BLOOD_TYPE_CHOICE)
    phone = models.CharField(_("Phone"), max_length=10)
    address = models.TextField(_("Address"))
    public_health_id = models.ForeignKey(Public_Health, verbose_name=_("Creator ID"), on_delete=models.DO_NOTHING)
    date = models.DateField(_("Created Date"), auto_now=True)

    def age(self):
        return int((datetime.date.today() - self.birth_day).days / 365.25 )
    age = property(age)


class Congenital_disease(models.Model):
    name = models.CharField(_("Congenital disease name"), max_length=255)
    patient_id = models.ManyToManyField(Patient, verbose_name=_("Patient ID"))

