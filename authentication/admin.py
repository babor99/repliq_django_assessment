from django.contrib import admin
from django.contrib.auth.models import Group

from .models import *


@admin.register(User)
class UserAdmin(admin.ModelAdmin):
	list_display = [field.name for field in User._meta.fields]


@admin.register(Employee)
class EmployeeAdmin(admin.ModelAdmin):
	list_display = [field.name for field in Employee._meta.fields]


@admin.register(Role)
class RoleAdmin(admin.ModelAdmin):
	list_display = [field.name for field in Role._meta.fields]


@admin.register(Permission)
class PermissionAdmin(admin.ModelAdmin):
	list_display = [field.name for field in Permission._meta.fields]


admin.site.unregister(Group)
