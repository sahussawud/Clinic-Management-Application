from webbrowser import register

from django.contrib import admin
from .models import *
# Register your models here.
class TreatmentAdmin(admin.ModelAdmin):
    list_display = ['cn', 'med_cer', 'patient_condition', 'create_date']
    list_per_page = 10
    list_filter = ['med_cer', 'patient_condition']
    search_fields = ['cn', 'create_date']

admin.site.register(Treatment, TreatmentAdmin)
class DiagnosisAdmin(admin.ModelAdmin):
    list_per_page = 10
    list_filter = ['icd_10', 'doctor_id']
    search_fields = ['icd_10', 'doctor_id']

admin.site.register(Diagnosis, DiagnosisAdmin)
class Icd_10Admin(admin.ModelAdmin):
    list_display = ['code', 'detail']
    list_per_page = 10
    list_filter = ['code', 'detail']
    search_fields = ['code', 'detail']
admin.site.register(Icd_10, Icd_10Admin)

class SymptomAdmin(admin.ModelAdmin):
    list_per_page = 10
admin.site.register(Symptom, SymptomAdmin)

class PrescriptionAdmin(admin.ModelAdmin):
    list_per_page = 10
admin.site.register(Prescription, PrescriptionAdmin)

class Room_QueueAdmin(admin.ModelAdmin):
    list_per_page = 10
admin.site.register(Room_Queue, Room_QueueAdmin)

