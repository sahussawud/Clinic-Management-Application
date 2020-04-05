from django.contrib.auth.models import User
from django.db import models
from django.utils.translation import gettext_lazy as _
from django.conf import settings
from User_app.models import Patient, Nurse
# Create your models here.

class Treatment(models.Model):
    cn = models.IntegerField(_("Clinic number"), primary_key=True)
    weight = models.FloatField(_("Weight"))
    Height = models.FloatField(_("Height"))
    bp = models.IntegerField(_("Blood pressures"))
    pr = models.IntegerField(_("Pulse rates"))
    temp = models.FloatField(_("Temperatures"))
    rr = models.IntegerField(_("Respiratory rates"))
    bmi = models.FloatField(_("BMI"))
    o2_sat = models.IntegerField(_("Oxygen saturation"))
    med_cer = models.BooleanField(_("Medical certificate"))
    follow_up = models.DateField(_("Follow up ?"), auto_now=False, auto_now_add=False)
    PATIENT_CONDITION_CHOICE = [
        ('SC', 'Selfcome'),
        ('AB', 'Ambulance'),
        ('ST', 'Stretcher')
    ] 
    patient_condition = models.CharField(_("Patient Condition"), max_length=2, choices=PATIENT_CONDITION_CHOICE)
    current_history = models.CharField(_("Current History"), max_length=255)
    date = models.DateField(_(""), auto_now=True)
    important_symptom = models.CharField(_("Important Symptom"), max_length=255)
    detail = models.CharField(_("Detail"), max_length=255)
    user_id = models.OneToOneField(settings.AUTH_USER_MODEL, verbose_name=_("Creator user"), on_delete=models.CASCADE)
    patient_p_id = models.ForeignKey(Patient, verbose_name=_("Patient ID"), on_delete=models.CASCADE)

class Symptom(models.Model):
    name = models.CharField(_("Symtom name"), max_length=255)

class Symptom_detail(models.Model):
    treatment_cn = models.ForeignKey(Treatment, verbose_name=_("Treatment Clinic number"), on_delete=models.CASCADE)
    symptom_id = models.OneToOneField(Symptom, verbose_name=_("Symptom ID"), on_delete=models.CASCADE)

class Diagnosis(models.Model):
    diagnosis_detail = models.CharField(_("Diagnosis detail"), max_length=255)
    symptom_detail_id = models.ManyToManyField(Symptom_detail, verbose_name=_("Symptom Detail ID"))

class Treatment_method(models.Model):
    detail = models.CharField(_("Treatment method detail"), max_length=255)
    symptom_detail_id = models.ManyToManyField(Symptom_detail, verbose_name=_("Symptom Detail ID"))

class Prescription(models.Model):
    detail = models.CharField(_("Prescription detail"), max_length=255)
    nurse_id = models.ForeignKey(Nurse, verbose_name=_("Creator ID"), on_delete=models.CASCADE)
    treatment_cn = models.OneToOneField(Treatment, verbose_name=_("Treatment Clinic number"), on_delete=models.CASCADE)
    