from django.contrib import admin

from .models import *


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
	list_display = [field.name for field in Category._meta.fields]


@admin.register(Device)
class DeviceAdmin(admin.ModelAdmin):
	list_display = [field.name for field in Device._meta.fields]


@admin.register(DeviceAssign)
class DeviceAssignAdmin(admin.ModelAdmin):
	list_display = [field.name for field in DeviceAssign._meta.fields]


@admin.register(DeviceReturn)
class DeviceReturnAdmin(admin.ModelAdmin):
	list_display = [field.name for field in DeviceReturn._meta.fields]


@admin.register(DeviceLog)
class DeviceLogAdmin(admin.ModelAdmin):
	list_display = [field.name for field in DeviceLog._meta.fields]

