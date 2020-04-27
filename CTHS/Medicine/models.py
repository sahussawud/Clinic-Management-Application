from django.contrib.auth.models import User
from django.db import models
from django.utils.translation import gettext_lazy as _
from django.conf import settings
from Treatment.models import Prescription
from User_app.models import Patient
# Create your models here.

class Med_supply(models.Model):
    med_sup_id = models.AutoField(_("Medical supply ID"), primary_key=True)
    sup_id = models.CharField(_("Medical Supply ID"), max_length=24, null=True)
    name = models.CharField(_("Medical supply name"), max_length=255)
    description = models.CharField(_("Medical Supply Description"), max_length=255, default="")
    amount = models.IntegerField(_("Amount left"))

class Drug(models.Model):
    med_sup_id = models.AutoField(_("Drug ID"), primary_key=True)
    drug_id = models.CharField(_("Drug ID"), max_length=24, null=True)
    description = models.CharField(_("Drug Description"), max_length=255, default="")
    name = models.CharField(_("Drug name"), max_length=255)
    amount = models.IntegerField(_("Amount left"))
    patient = models.ManyToManyField(Patient, verbose_name=_("Allergic Drug(s)"))

class Dispense(models.Model):
    amount =  models.IntegerField(_("Amount"))
    DISPENSE_TYPE_CHOICE = [
        ('D', 'ยา'),
        ('M', 'เวชภัณฑ์')
    ]
    type = models.CharField(_("Dispense type"), max_length=1, choices=DISPENSE_TYPE_CHOICE)
    prescription_id = models.ForeignKey(Prescription, verbose_name=_("Prescription ID"), on_delete=models.CASCADE)
    dis_med_id = models.ForeignKey(Med_supply, verbose_name=_("Dispense ID"), on_delete=models.CASCADE, null=True, blank=True)
    dis_drug_id = models.ForeignKey(Drug, verbose_name=_("Dispense ID"), on_delete=models.CASCADE, null=True, blank=True)
