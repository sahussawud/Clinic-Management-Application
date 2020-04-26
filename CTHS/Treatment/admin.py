from webbrowser import register

from django.contrib import admin
from .models import *
# Register your models here.
admin.site.register(Treatment)
admin.site.register(Diagnosis)
admin.site.register(Icd_10)
admin.site.register(Symptom)
admin.site.register(Lesion)

