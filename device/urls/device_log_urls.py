from django.urls import path
from device.views import device_log_views as views


urlpatterns = [
	path('api/v1/device_log/all/', views.getAllDeviceLog),

	path('api/v1/device_log/without_pagination/all/', views.getAllDeviceLogWithoutPagination),

	path('api/v1/device_log/<int:pk>', views.getADeviceLog),

	path('api/v1/device_log/search/', views.searchDeviceLog),

	path('api/v1/device_log/create/', views.createDeviceLog),

	path('api/v1/device_log/update/<int:pk>', views.updateDeviceLog),

	path('api/v1/device_log/delete/<int:pk>', views.deleteDeviceLog),
]