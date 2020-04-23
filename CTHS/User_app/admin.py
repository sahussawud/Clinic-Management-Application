from django.contrib import admin
from .models import Public_Health, User, Congenital_disease
# Register your models here.

admin.site.register(User)
admin.site.register(Public_Health)
admin.site.register(Congenital_disease)