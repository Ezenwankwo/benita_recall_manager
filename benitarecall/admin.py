from django.contrib import admin
from .models import Patient, Schedule

# Register your models here.

admin.site.register(Patient)
admin.site.register(Schedule)
