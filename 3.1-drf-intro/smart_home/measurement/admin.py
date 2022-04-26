from django.contrib import admin

# Register your models here.
from measurement.models import Measurement, Sensor


@admin.register(Sensor)
class OrderAdmin(admin.ModelAdmin):
    list_display = ['name', 'description']  # measurements


@admin.register(Measurement)
class OrderAdmin(admin.ModelAdmin):
    list_display = ['id', 'temperature', 'created_at']
