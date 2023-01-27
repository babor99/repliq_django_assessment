from django.urls import path
from device.views import device_log_views as views


urlpatterns = [
	path('api/v1/device_log/all/', views.getAllDeviceLog),
	path('api/v1/get_all_company_device_log/', views.getAllDeviceLogByCompany),
	path('api/v1/get_all_company_device_log/<int:device_id>', views.getAllDeviceLogByDeviceId),

	path('api/v1/device_log/<int:pk>', views.getADeviceLog),
	path('api/v1/company_device_log/<int:pk>', views.getADeviceLogByCompany),

	path('api/v1/device_log/search/', views.searchDeviceLog),
	path('api/v1/search_company_device_log/', views.searchDeviceLogByCompany),

	path('api/v1/device_log/create/', views.createDeviceLog),

	path('api/v1/device_log/update/<int:pk>', views.updateDeviceLog),
	path('api/v1/update_company_device_log/<int:pk>', views.updateDeviceLogByCompany),

	path('api/v1/device_log/delete/<int:pk>', views.deleteDeviceLog),
	path('api/v1/delete_company_device_log/<int:pk>', views.deleteDeviceLogByCompany),
]