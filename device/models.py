from django.db import models

from commons.mixins import CreatedUpdatedModelMixin
from authentication.models import Employee, User




class Category(CreatedUpdatedModelMixin):
    name = models.CharField(max_length=255)
    company = models.ForeignKey(User, on_delete=models.CASCADE, related_name='company_categories')

    class Meta:
        ordering = ('-id',)
        verbose_name_plural = 'Category'

    def __str__(self):
        return self.name




class Device(CreatedUpdatedModelMixin):
    name = models.CharField(max_length=255)
    company = models.ForeignKey(User, on_delete=models.CASCADE, related_name='company_devices')
    category = models.ForeignKey(Category, on_delete=models.SET_NULL, null=True, blank=True)
    description = models.TextField(null=True, blank=True)

    class Meta:
        ordering = ('-id',)
        verbose_name_plural = 'Device'

    def __str__(self):
        return self.name




class DeviceAssign(CreatedUpdatedModelMixin):
    device = models.ForeignKey(Device, on_delete=models.CASCADE, related_name='device_assigns')
    company = models.ForeignKey(User, on_delete=models.CASCADE, related_name='company_device_assigns')
    employee = models.ForeignKey(Employee, on_delete=models.CASCADE, related_name='employee_assign_devices')
    condition = models.TextField()

    start_date = models.DateTimeField()
    end_date = models.DateTimeField()

    class Meta:
        ordering = ('-id',)
        verbose_name_plural = 'DeviceAssign'

    def __str__(self):
        return f"{self.employee.full_name}: {self.device.name[:15]}"




class DeviceReturn(CreatedUpdatedModelMixin):
    device = models.ForeignKey(Device, on_delete=models.CASCADE, related_name='device_returns')
    company = models.ForeignKey(User, on_delete=models.CASCADE, related_name='company_device_returns')
    employee = models.ForeignKey(Employee, on_delete=models.CASCADE, related_name='employee_return_devices')
    condition = models.TextField()

    return_date = models.DateTimeField()

    class Meta:
        ordering = ('-id',)
        verbose_name_plural = 'DeviceReturn'

    def __str__(self):
        return f"{self.employee.full_name}: {self.device.name[:15]}"




class DeviceLog(CreatedUpdatedModelMixin):
    type = models.CharField(max_length=255)
    device = models.ForeignKey(Device, on_delete=models.CASCADE, related_name='device_logs')
    company = models.ForeignKey(User, on_delete=models.CASCADE, related_name='company_device_logs')
    description = models.TextField(null=True, blank=True)

    class Meta:
        ordering = ('-id',)
        verbose_name_plural = 'DeviceLog'

    def __str__(self):
        return self.name


