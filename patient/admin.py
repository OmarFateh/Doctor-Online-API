from django.contrib import admin

from .models import Patient


# models admin site registeration
admin.site.register(Patient)