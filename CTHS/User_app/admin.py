from django.contrib import admin
from .models import *
from django.contrib.auth.models import Permission
from .models import Public_Health, User, Congenital_disease
from Treatment.models import Treatment, Diagnosis, Symptom, Icd_10, Non_Form_Symptom
# Register your models here.
class UserAdmin(admin.ModelAdmin):
    list_display = ['id', 'first_name', 'last_name']
    list_per_page = 10
    search_fields = ['first_name', 'last_name']
admin.site.register(User, UserAdmin)

admin.site.register(Permission)
admin.site.register(Patient)
class Public_HealthAdmin(admin.ModelAdmin):
    list_per_page = 10
admin.site.register(Public_Health, Public_HealthAdmin)

class DoctorAdmin(admin.ModelAdmin):
    list_per_page = 10
admin.site.register(Doctor, DoctorAdmin)

class NurseAdmin(admin.ModelAdmin):
    list_per_page = 10
admin.site.register(Nurse, NurseAdmin)

class Congenital_diseaseAdmin(admin.ModelAdmin):
    list_per_page = 10
admin.site.register(Congenital_disease, Congenital_diseaseAdmin)
