from django.contrib import admin
from .models import *
from django.contrib.auth.models import Permission
# Register your models here.

admin.site.register(User)
admin.site.register(Permission)
admin.site.register(Public_Health)
admin.site.register(Doctor)
admin.site.register(Nurse)
admin.site.register(Congenital_disease)