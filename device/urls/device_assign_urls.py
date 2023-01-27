from django.urls import path
from device.views import device_assign_views as views


urlpatterns = [
	path('api/v1/device_assign/all/', views.getAllDeviceAssign),

	path('api/v1/device_assign/without_pagination/all/', views.getAllDeviceAssignWithoutPagination),

	path('api/v1/device_assign/<int:pk>', views.getADeviceAssign),

	path('api/v1/device_assign/search/', views.searchDeviceAssign),

	path('api/v1/device_assign/create/', views.createDeviceAssign),

	path('api/v1/device_assign/update/<int:pk>', views.updateDeviceAssign),

	path('api/v1/device_assign/delete/<int:pk>', views.deleteDeviceAssign),
]