from django.contrib import admin
from .models import Public_Health, User, Congenital_disease
from Treatment.models import Treatment, Diagnosis, Symptom, Icd_10, Non_Form_Symptom
# Register your models here.

admin.site.register(User)
admin.site.register(Public_Health)
admin.site.register(Congenital_disease)
admin.site.register(Treatment)
admin.site.register(Diagnosis)
admin.site.register(Symptom)
admin.site.register(Icd_10)
admin.site.register(Non_Form_Symptom)
