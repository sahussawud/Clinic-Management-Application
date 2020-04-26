from django.contrib import admin
from .models import *
from django.contrib.auth.models import Permission
from .models import Public_Health, User, Congenital_disease
from Treatment.models import Treatment, Diagnosis, Symptom, Icd_10, Non_Form_Symptom
# Register your models here.

admin.site.register(User)
admin.site.register(Permission)
admin.site.register(Public_Health)
admin.site.register(Doctor)
admin.site.register(Nurse)
admin.site.register(Congenital_disease)
admin.site.register(Non_Form_Symptom)
