from django.urls import path
from device.views import device_assign_views as views


urlpatterns = [
	path('api/v1/device_assign/all/', views.getAllDeviceAssign),
	path('api/v1/get_all_by_company/', views.getAllDeviceAssignByCompany),

	path('api/v1/device_assign/<int:pk>', views.getADeviceAssign),
	path('api/v1/get_device_assign/<int:pk>', views.getADeviceAssignByCompany),

	path('api/v1/device_assign/search/', views.searchDeviceAssign),
	path('api/v1/search_company_device_assign/', views.searchDeviceAssignByCompany),

	path('api/v1/device_assign/create/', views.createDeviceAssign),

	path('api/v1/device_assign/update/<int:pk>', views.updateDeviceAssign),
	path('api/v1/update_company_device_assign/<int:pk>', views.updateDeviceAssignByCompany),

	path('api/v1/device_assign/delete/<int:pk>', views.deleteDeviceAssign),
	path('api/v1/delete_company_device_assign/<int:pk>', views.deleteDeviceAssignByCompany),
]