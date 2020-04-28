from django.contrib.auth.models import User
from django.db import models
from django.utils.translation import gettext_lazy as _
from django.conf import settings
from User_app.models import Patient, Nurse, Doctor
# Create your models here.
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
class Icd_10(models.Model):
    code = models.CharField(_("code"), max_length=25)
    detail = models.CharField(_("detail"), max_length=255)
    symptom_type = models.CharField(_("symptom_type"), max_length=12, choices=SYMPTOM_TYPE)

class Treatment(models.Model):
    cn = models.AutoField(_("Clinic number"), primary_key=True)
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
        ('SC', 'มาด้วยตนเอง'),
        ('AB', 'รถพยาบาล'),
        ('ST', 'เปลนอน')
    ] 
    patient_condition = models.CharField(_("Patient Condition"), max_length=2, choices=PATIENT_CONDITION_CHOICE, default='SC')
    # current_history = models.CharField(_("Current History"), max_length=255)
    create_date = models.DateField(_(""), auto_now=True)
    

    def bmi(self):
        return  self.weight / self.Height**2
    bmi = property(bmi)
    
    user_id = models.ForeignKey(settings.AUTH_USER_MODEL, verbose_name=_("Creator user"), on_delete=models.CASCADE) #change from o2o to foriegnfield
    patient_p_id = models.ForeignKey(Patient, verbose_name=_("PatientID"), on_delete=models.CASCADE)

class Diagnosis(models.Model):
    icd_10 = models.ManyToManyField(Icd_10, verbose_name=_("icd_10s"))
    diagnosis_detail = models.CharField(_("คำวินิฉัย"), max_length=255, blank=True)
    advice = models.CharField(_("คำเเนะนำ"), max_length=255, blank=True)
    doctor_id = models.ForeignKey(Doctor, verbose_name=_("Diagnos Doctor"), on_delete=models.CASCADE)
    follow_up = models.DateField(_("วันนัด"), null=True)
    follow_up_for = models.CharField(_("เพื่อ"), max_length=100, blank=True)
    treatment = models.OneToOneField(Treatment, verbose_name=_("Treatment ID"), on_delete=models.CASCADE, null=True)

class Symptom(models.Model):
    treatment = models.OneToOneField(Treatment, verbose_name=_("Treatment"), on_delete=models.CASCADE)
    symptom_type = models.CharField(_("symptom_type"), max_length=12, choices=SYMPTOM_TYPE, null=True)

class Prescription(models.Model):
    detail = models.CharField(_("Prescription detail"), max_length=255, blank=True)
    doctor_id = models.ForeignKey(Doctor, verbose_name=_("Creator ID"), on_delete=models.CASCADE, null=True)
    treatment_cn = models.OneToOneField(Treatment, verbose_name=_("Treatment Clinic number"), on_delete=models.CASCADE)
    PRESCRIPTION_STATUS_CHOICE = [
        ('C', 'จ่ายยาแล้ว'),
        ('W', 'รอการจ่ายยา')
    ]
    status = models.CharField(_("Prescription Status"), max_length=1, choices=PRESCRIPTION_STATUS_CHOICE, default="W")
    nurse_id = models.ForeignKey(Nurse, verbose_name=_("พยาบาลผู้จ่ายยา"), on_delete=models.CASCADE, null=True)

class Non_Form_Symptom(models.Model):
    symptom = models.OneToOneField(Symptom, verbose_name=_("Symptom ID"), on_delete=models.CASCADE)
    important_symptom = models.CharField(_("อาการสำคัญ"),max_length=255)
    current_history = models.CharField(_("ประวัติปัจจุบัน"),max_length=255)

class Rash_Symptom(models.Model):
    symptom = models.OneToOneField(Symptom, verbose_name=_("Symptom ID"), on_delete=models.CASCADE)
    rash_area = models.CharField(_("ผื่นบริเวณ"), max_length=255)
    rash_date = models.IntegerField(_("เป็นมานาน (วัน)"), default=1)
    itch = models.BooleanField(_("คัน"), default=False)
    pain = models.BooleanField(_("ปวด"), default=False)
    sting = models.BooleanField(_("เเสบ"), default=False)
    fever = models.BooleanField(_("ไข้"), default=False)
    swell = models.BooleanField(_("บวม"), default=False)
    rash_detail = models.CharField(_("สัมผัสโดน"), max_length=255)
    pe = models.CharField(_("PE"), max_length=255)

class Wound_Symptom(models.Model):
    symptom = models.OneToOneField(Symptom, verbose_name=_("Symptom ID"), on_delete=models.CASCADE)
    emergency = models.BooleanField(_('ผู้ป่วยฉุกเฉิน'),default=False)
    insurance = models.BooleanField(_("เบิกประกันอุบัติเหตุ"), default=False)
    is_safety = models.BooleanField(_("สวมหมวกันน็อค/คาดเข็มขัด"), default=False)
    wound_area = models.CharField(_("บาดเเผลบริเวณ"), max_length=255)
    wound_date = models.DateField(_("วันที่เกิดเหตุ"))
    wound_locale = models.CharField(_("สถานที่เกิดเหตุ"), max_length=255)
    is_treat_before = models.BooleanField(_("เคยเข้ารับการรักมาเเล้ว"), default=False)
    treatment_before_detail = models.CharField(_("ที่"), max_length=255, blank=True)
    time = models.TimeField(_("เวลา"), blank=True)


class Lesion(models.Model):
    wound_symptom = models.ForeignKey(Wound_Symptom, on_delete=models.CASCADE)
    AREA_TYPE_CHOICE = [
        ('1', 'ถลอก'),
        ('2', 'ฉีกขาด'),
        ('3', 'จากของมีคม'),
        ('4', 'อื่นๆ'),
    ]
    lesion_type = models.CharField(_("บาดแผล"), max_length=1, choices=AREA_TYPE_CHOICE)
    lesion_area = models.CharField(_("บริเวณ"), max_length=100)
    lesion_x = models.IntegerField(_("กว้าง"))
    lesion_y = models.IntegerField(_("ยาว"))

class Con_Wound_Symptom(models.Model):
    symptom = models.OneToOneField(Symptom, verbose_name=_("Symptom ID"), on_delete=models.CASCADE, null=True)
    LESION = [
        ('1','เเย่ลง'),
        ('2','เท่าเดิม'),
        ('3','ดีขึ้น')
    ]
    insurance = models.BooleanField(_("ผู้ป่วยเบิกประกัน"), default=False)
    detail = models.CharField(_("ลักษณะบาดเเผล"), max_length=1 , choices=LESION, default=LESION[1][0])
    advice = models.CharField(_("คำเเนะนำ"), max_length=100,blank=True)
    more = models.CharField(_("เพิ่มเติ่ม"), max_length=100)

    
class Eye_Symptom(models.Model):
    symptom = models.OneToOneField(Symptom, verbose_name=_("Symptom ID"), on_delete=models.CASCADE)
    left = models.BooleanField(_("ตาซ้าย"), default=False)
    right = models.BooleanField(_("ตาขวา"), default=False)
    pain = models.BooleanField(_("ปวดตา"), default=False)
    irritation = models.BooleanField(_("เคืองตา"), default=False)
    itch = models.BooleanField(_("คันตา"), default=False)
    conjunctivitis = models.BooleanField(_("ตาเเดง"), default=False)
    sore = models.BooleanField(_("เจ็บหนังตา"), default=False)
    swoll = models.BooleanField(_("หนังตาบวม"), default=False)
    tear = models.BooleanField(_("น้ำตาไหล"), default=False)
    blurred = models.BooleanField(_("ตาพร่ามัว"), default=False)
    gum = models.BooleanField(_("ขี้ตาเยอะ"), default=False)
    purulent = models.BooleanField(_("ขี้ตาเป็นหนอง"), default=False)
    matter = models.BooleanField(_("สิ่งเเปลกปลอมเข้าดวงตา"), default=False)
    check_up = models.CharField(_("ตรวจร่างกาย"), max_length=255, blank=True)

class Fever_Symptom(models.Model):
    symptom = models.OneToOneField(Symptom, verbose_name=_("Symptom ID"), on_delete=models.CASCADE)
    fever = models.BooleanField(_("ไข้"))
    cough = models.BooleanField(_("ไอ"))
    phlegm = models.BooleanField(_("เสมหะ"))
    snot = models.BooleanField(_("น้ำมูก"))
    headache = models.BooleanField(_("ปวดศีรษะ"))
    stuffy = models.BooleanField(_("คัดจมูก"))
    food_bored = models.BooleanField(_("เบื่ออาหาร"))
    body_aches = models.BooleanField(_("ปวดเมื่อยตามตัว"))
    sore_throat = models.BooleanField(_("เจ็บคอ"))
    eye_itch = models.BooleanField(_("คันตา"))

    injected_pharynx = models.BooleanField(_("Injected pharynx"))
    exudates = models.BooleanField(_("Exudates"))
    lungs = models.BooleanField(_("Lungs : Clear"))
    more = models.CharField(_("เพิ่มเติ่ม"), max_length=255, blank=True)

class Diarrhea_Symptom(models.Model):
    symptom = models.OneToOneField(Symptom, verbose_name=_("Symptom ID"), on_delete=models.CASCADE)
    diarrhea_amount = models.IntegerField(_("จำนวนครั้งในการถ่าย"), default=0)
    diarrhea_detail = models.CharField(_("อุจจาระลักษณะ"), max_length=255 , blank=True, default="")

    stomachache = models.CharField(_("ลักษณะการปวดท้อง"), max_length=255, blank=True, default='')
    vomit = models.BooleanField(_("คลื่นไส้/อาเจียน"), default=False)
    flux_stool = models.BooleanField(_("อุจาระมีมูลเลือด"), default=False)
    fever = models.BooleanField(_("ไข้"), default=False)
    
    bowel_sound = models.CharField(_("bowel sound"), max_length=255, blank=True, default='')
    current_history = models.CharField(_("ประวัติปัจจุบัน"), max_length=255, blank=True, default='')

class Pain_Symptom(models.Model):
    symptom = models.OneToOneField(Symptom, verbose_name=_("Symptom ID"), on_delete=models.CASCADE)
    bodyache_area = models.CharField(_("ปวดบริเวณ"), max_length=255)
    bodyache_date = models.IntegerField(_("เป็นมานาน (วัน)"))
    pain_score = models.IntegerField(_("Pain score"))
    ache_detail = models.CharField(_("ลักษณะการปวด"), max_length=255)
    trigger =  models.CharField(_("สิ่งที่กระตุ้น/สิ่งที่บรรเทา"), max_length=255)
    crack = models.CharField(_("ร้าวไป"), max_length=255)
    others = models.CharField(_("อาการอื่น"), max_length=255)

class Room_Queue(models.Model):
    treatment = models.ForeignKey(Treatment, verbose_name=_("Treatment ID"), on_delete=models.CASCADE)
    ROOM_QUEUE_STATUS = [
        ('WD', 'รอเข้าห้องตรวจ'),
        ('WP', 'รอการจ่ายยา')
    ]
    status = models.CharField(_("Queue status"), max_length=2, choices=ROOM_QUEUE_STATUS, default="WD")