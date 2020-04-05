from django.contrib.auth.models import User
from django.db import models
from django.utils.translation import gettext_lazy as _
from django.conf import settings
from Treatment.models import Prescription
from User_app.models import Patient
# Create your models here.

class Dispense(models.Model):
    amount =  models.IntegerField(_("Amount"))
    DISPENSE_TYPE_CHOICE = [
        ('D', 'dis_drug'),
        ('M', 'dis_med')
    ]
    type = models.CharField(_("Dispense type"), max_length=1, choices=DISPENSE_TYPE_CHOICE)
    prescription_id = models.ForeignKey(Prescription, verbose_name=_("Prescription ID"), on_delete=models.CASCADE)

class Med_supply(models.Model):
    med_sup_id = models.IntegerField(_("Medical supply ID"), primary_key=True)
    name = models.CharField(_("Medical supply name"), max_length=255)
    amount = models.IntegerField(_("Amount left"))
    dis_med_id = models.ManyToManyField(Dispense, verbose_name=_("Dispense ID"))

class Drug(models.Model):
    med_sup_id = models.IntegerField(_("Drug ID"), primary_key=True)
    name = models.CharField(_("Drug name"), max_length=255)
    amount = models.IntegerField(_("Amount left"))
    dis_med_id = models.ManyToManyField(Dispense, verbose_name=_("Dispense ID"))
    patient = models.ManyToManyField(Patient, verbose_name=_("Allergic Drug(s)"))

    
