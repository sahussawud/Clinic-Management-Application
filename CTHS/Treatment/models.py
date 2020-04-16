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
    
class Rash_diagnosis(models.Model):
    diagnosis_id = models.OneToOneField(Diagnosis, verbose_name=_("Diagnosis ID"), on_delete=models.CASCADE)
    rash_area = models.CharField(_("Rash Area"), max_length=255)
    rash_date = models.IntegerField(_("How long ? (day)"))
    itch = models.BooleanField(_("Itch"))
    pain = models.BooleanField(_("Pain"))
    sting = models.BooleanField(_("Sting"))
    fever = models.BooleanField(_("Fever"))
    swell = models.BooleanField(_("Swell"))
    rash_detail = models.CharField(_("Rash Detail"), max_length=255)
    pe = models.CharField(_("PE"), max_length=255)

class Wound_diagnosis(models.Model):
    diagnosis_id = models.OneToOneField(Diagnosis, verbose_name=_("Diagnosis ID"), on_delete=models.CASCADE)
    helmet = models.BooleanField(_("Is helmet on ?"))
    seatbelt = models.BooleanField(_("Is seatbelt on ?"))
    wound_detail = models.CharField(_("Wound Detail"), max_length=255)
    WOUND_AREA_TYPE_CHOICE = [
        ('1', 'Scratched'),
        ('2', 'Tear'),
        ('3', 'From Sharp object'),
        ('4', 'Others')
    ]
    wound_type = models.CharField(_("Rash Type"), max_length=1, choices=WOUND_AREA_TYPE_CHOICE)
    wound_area = models.CharField(_("Wound Area"), max_length=255)
    wound_size = models.CharField(_("Wound Size"), max_length=255)
    wound_date = models.DateField(_("Date of accident"), auto_now=False, auto_now_add=False)
    wound_locale = models.CharField(_("Locale of accident"), max_length=255)
    TREATMENT_BEFORE_CHOICE = [
        ('N', 'Never had treatment before'),
        ('Y', 'Had treatment before')
    ]
    treatment_before = models.CharField(_("Had treatment before ?"), max_length=1, choices=TREATMENT_BEFORE_CHOICE)
    treatment_before_detail = models.CharField(_("Last treatment detail"), max_length=255)
    doctor_fee = models.IntegerField(_("Doctor fee"))
    
class Eye_diagnosis(models.Model):
    diagnosis_id = models.OneToOneField(Diagnosis, verbose_name=_("Diagnosis ID"), on_delete=models.CASCADE)
    left = models.BooleanField(_("Left"))
    right = models.BooleanField(_("Right"))
    pain = models.BooleanField(_("Pain"))
    irritation = models.BooleanField(_("Irritation"))
    itch = models.BooleanField(_("Itch"))
    conjunctivitis = models.BooleanField(_("Conjunctivitis"))
    sore = models.BooleanField(_("Sore Eyelids"))
    swoll = models.BooleanField(_("Swollen Eyelids"))
    tear = models.BooleanField(_("Teary"))
    blurred = models.BooleanField(_("Blurred Vision"))
    gum = models.BooleanField(_("Gum in the eye"))
    purulent = models.BooleanField(_("Purulent eye"))
    matter = models.BooleanField(_("Foreign matter into the eye"))
    check_up = models.CharField(_("Check up"), max_length=255)

class Fever_diagnosis(models.Model):
    diagnosis_id = models.OneToOneField(Diagnosis, verbose_name=_("Diagnosis ID"), on_delete=models.CASCADE)
    fever = models.BooleanField(_("Fever"))
    cough = models.BooleanField(_("Cough"))
    phlegm = models.BooleanField(_("Phlegm"))
    snot = models.BooleanField(_("Snot"))
    headache = models.BooleanField(_("Headache"))
    stuffy = models.BooleanField(_("Stuffy Nose"))
    food_bored = models.BooleanField(_("Bored with food"))
    body_aches = models.BooleanField(_("Body aches"))
    sore_throat = models.BooleanField(_("Sore throat"))
    eye_itch = models.BooleanField(_("Eye itching"))
    injected_pharynx = models.BooleanField(_("Injected pharynx"))
    exudates = models.BooleanField(_("Exudates"))
    lungs = models.BooleanField(_("Lungs : Clear"))

class Diarrhea_diagnosis(models.Model):
    diagnosis_id = models.OneToOneField(Diagnosis, verbose_name=_("Diagnosis ID"), on_delete=models.CASCADE)
    diarrhea_detail = models.CharField(_("Diarrhea detail"), max_length=255)
    stomachache = models.CharField(_("Stomachache"), max_length=255)
    vomit = models.BooleanField(_("Squeamish / Vomit"))
    flux_stool = models.BooleanField(_("Flux stool"))
    fever = models.BooleanField(_("Fever"))
    symptom_detail = models.CharField(_("Symptom detail"), max_length=255)

class Bodyache_diagnosis(models.Model):
    diagnosis_id = models.OneToOneField(Diagnosis, verbose_name=_("Diagnosis ID"), on_delete=models.CASCADE)
    bodyache_area = models.CharField(_("Symptom detail"), max_length=255)
    bodyache_date = models.IntegerField(_("How long ? (day)"))
    pain_score = models.IntegerField(_("Pain score"))
    ache_detail = models.CharField(_("Ache detail"), max_length=255)
    trigger =  models.CharField(_("Stimulus/Relief"), max_length=255)
    crack = models.CharField(_("Crack"), max_length=255)
    others = models.CharField(_("Other symtoms"), max_length=255)
