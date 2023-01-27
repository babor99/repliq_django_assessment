from django.urls import path
from device.views import device_return_views as views


urlpatterns = [
	path('api/v1/device_return/all/', views.getAllDeviceReturn),

	path('api/v1/device_return/without_pagination/all/', views.getAllDeviceReturnWithoutPagination),

	path('api/v1/device_return/<int:pk>', views.getADeviceReturn),

	path('api/v1/device_return/search/', views.searchDeviceReturn),

	path('api/v1/device_return/create/', views.createDeviceReturn),

	path('api/v1/device_return/update/<int:pk>', views.updateDeviceReturn),

	path('api/v1/device_return/delete/<int:pk>', views.deleteDeviceReturn),
]