from django.contrib.auth.models import User
from django.db import models
from django.utils.translation import gettext_lazy as _
from django.conf import settings
from User_app.models import Patient, Nurse, Doctor
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
    # follow_up = models.DateField(_("Follow up ?"), auto_now=False, auto_now_add=False)
    PATIENT_CONDITION_CHOICE = [
        ('SC', 'Selfcome'),
        ('AB', 'Ambulance'),
        ('ST', 'Stretcher')
    ] 
    patient_condition = models.CharField(_("Patient Condition"), max_length=2, choices=PATIENT_CONDITION_CHOICE)
    # current_history = models.CharField(_("Current History"), max_length=255)
    create_date = models.DateField(_(""), auto_now=True) #change name
    # important_symptom = models.CharField(_("Important Symptom"), max_length=255)
    # detail = models.CharField(_("Detail"), max_length=255)
    
    user_id = models.name = models.ForeignKey(settings.AUTH_USER_MODEL, verbose_name=_("Creator user"), on_delete=models.CASCADE) #change from o2o to foriegnfield
    patient_p_id = models.ForeignKey(Patient, verbose_name=_("PatientID"), on_delete=models.CASCADE)

class Symptom(models.Model):
    treatment = models.OneToOneField(Treatment, verbose_name=_("Treatment"), on_delete=models.CASCADE)
    SYMPTOM_TYPE = [
        ('non_form', 'ทั่วไป'),
        ('skin', 'ผิวหนัง'),
        ('accident', 'อุบัติเหตุ'),
        ('con_accident', 'อุบัติเหตุต่อเนื่อง'),
        ('eyes', 'ดวงตา'),
        ('fever', 'อาการไข้'),
        ('diarrhea', 'ท้องเสีย/ปวดท้อง'),
        ('pain', 'อาการปวดนอกเหนือ')
    ]
    symptom_type = models.CharField(_("symptom_type"), max_length=12, choices=SYMPTOM_TYPE)

class Icd_10(models.Model):
    code = models.CharField(_("code"), max_length=25)
    detail = models.CharField(_("detail"), max_length=255)

# class Symptom_detail(models.Model):
#     treatment_cn = models.ForeignKey(Treatment, verbose_name=_("Treatment Clinic number"), on_delete=models.CASCADE)
#     symptom_id = models.OneToOneField(Symptom, verbose_name=_("Symptom ID"), on_delete=models.CASCADE)

class Diagnosis(models.Model):
    icd_10 = models.ManyToManyField(Icd_10, verbose_name=_("icd_10s"))
    diagnosis_detail = models.CharField(_("Diagnosis detail"), max_length=255)
    advice = models.CharField(_("advice"), max_length=255)
    doctor_id = models.ForeignKey(Doctor, verbose_name=_("Diagnos Doctor"), on_delete=models.CASCADE)
    follow_up = models.DateField(_("Follow up"))
    follow_up_for = models.CharField(_("for"), max_length=100)


# class Treatment_method(models.Model):
#     detail = models.CharField(_("Treatment method detail"), max_length=255)
#     symptom_detail_id = models.ManyToManyField(Symptom_detail, verbose_name=_("Symptom Detail ID"))

class Prescription(models.Model):
    detail = models.CharField(_("Prescription detail"), max_length=255)
    nurse_id = models.ForeignKey(Nurse, verbose_name=_("Creator ID"), on_delete=models.CASCADE)
    treatment_cn = models.OneToOneField(Treatment, verbose_name=_("Treatment Clinic number"), on_delete=models.CASCADE)

class Non_Form_Symptom(models.Model):
    symptom = models.OneToOneField(Symptom, verbose_name=_("Symptom ID"), on_delete=models.CASCADE)
    important_symptom = models.CharField(_("อาการสำคัญ"),max_length=255)
    current_history = models.CharField(_("ประวัติปัจจุบัน"),max_length=255)

class Rash_Symptom(models.Model):
    symptom = models.OneToOneField(Symptom, verbose_name=_("Symptom ID"), on_delete=models.CASCADE)
    rash_area = models.CharField(_("ผื่นบริเวณ"), max_length=255)
    rash_date = models.IntegerField(_("เป็นมานาน (วัน)"))
    itch = models.BooleanField(_("คัน"))
    pain = models.BooleanField(_("ปวด"))
    sting = models.BooleanField(_("เเสบ"))
    fever = models.BooleanField(_("ไข้"))
    swell = models.BooleanField(_("บวม"))
    rash_detail = models.CharField(_("สัมผัสโดน"), max_length=255)
    pe = models.CharField(_("PE"), max_length=255)

class Wound_Symptom(models.Model):
    symptom = models.OneToOneField(Symptom, verbose_name=_("Symptom ID"), on_delete=models.CASCADE)
    insurance = models.BooleanField(_("เบิกประกัน"))
    is_safety = models.BooleanField(_("Is helmet on ?/Is seatbelt on ?"))
    wound_area = models.CharField(_("Wound Area"), max_length=255)
    wound_date = models.DateField(_("Date of accident"))
    wound_locale = models.CharField(_("Locale of accident"), max_length=255)

    is_treat_before = models.BooleanField(_("Had treatment before ?"))
    treatment_before_detail = models.CharField(_("Last treatment detail"), max_length=255)
    time = models.TimeField(_("เวลา"))


class Lesion(models.Model):
    wound_symptom = models.ForeignKey(Wound_Symptom, on_delete=models.CASCADE)
    AREA_TYPE_CHOICE = [
        ('1', 'Scratched'),
        ('2', 'Tear'),
        ('3', 'From Sharp object'),
        ('4', 'Others'),
    ]

    lesion_type = models.CharField(_("lesion_type"), max_length=1, choices=AREA_TYPE_CHOICE)
    lesion_area = models.CharField(_("บริเวณ"), max_length=100)
    lesion_x = models.IntegerField(_("กว้าง"))
    lesion_y = models.IntegerField(_("ยาว"))

class Con_Wound_Symptom(models.Model):
    LESION = [
        ('1','เเย่ลง'),
        ('2','เท่าเดิม'),
        ('3','ดีขึ้น')
    ]
    insurance = models.BooleanField(_("เบิกประกัน"))
    detail = models.CharField(_("ลักษณะบาดเเผล"), max_length=1 , choices=LESION )
    advice = models.CharField(_("คำเเนะนำ"), max_length=100)
    more = models.CharField(_("เพิ่มเติ่ม"), max_length=100)

    
class Eye_Symptom(models.Model):
    symptom = models.OneToOneField(Symptom, verbose_name=_("Symptom ID"), on_delete=models.CASCADE)
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

class Fever_Symptom(models.Model):
    symptom = models.OneToOneField(Symptom, verbose_name=_("Symptom ID"), on_delete=models.CASCADE)
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

class Diarrhea_Symptom(models.Model):
    symptom = models.OneToOneField(Symptom, verbose_name=_("Symptom ID"), on_delete=models.CASCADE)
    diarrhea_amount = models.IntegerField(_("จำนวนครั้ง"), default=0)
    diarrhea_detail = models.CharField(_("อุจจาระลักษณะ"), max_length=255 , blank=True, default="")

    stomachache = models.CharField(_("Stomachache"), max_length=255, blank=True, default='')
    vomit = models.BooleanField(_("Squeamish / Vomit"), default=False)
    flux_stool = models.BooleanField(_("Flux stool"), default=False)
    fever = models.BooleanField(_("Fever"), default=False)
    
    bowel_sound = models.CharField(_("bowel_sound"), max_length=255, blank=True, default='')

    current_history = models.CharField(_("bowel_sound"), max_length=255, blank=True, default='')

class Pain_Symptom(models.Model):
    symptom = models.OneToOneField(Symptom, verbose_name=_("Symptom ID"), on_delete=models.CASCADE)
    bodyache_area = models.CharField(_("ปวดบริเวณ"), max_length=255)
    bodyache_date = models.IntegerField(_("เป็นมานาน (วัน)"))
    pain_score = models.IntegerField(_("Pain score"))
    ache_detail = models.CharField(_("ลักษณะการปวด"), max_length=255)
    trigger =  models.CharField(_("สิ่งที่กระตุ้น/สิ่งที่บรรเทา"), max_length=255)
    crack = models.CharField(_("ร้าวไป"), max_length=255)
    others = models.CharField(_("อาการอื่น"), max_length=255)
