from django.urls import path
from device.views import device_views as views


urlpatterns = [
	path('api/v1/device/all/', views.getAllDevice),

	path('api/v1/device/without_pagination/all/', views.getAllDeviceWithoutPagination),

	path('api/v1/device/<int:pk>', views.getADevice),

	path('api/v1/device/search/', views.searchDevice),

	path('api/v1/device/create/', views.createDevice),

	path('api/v1/device/update/<int:pk>', views.updateDevice),

	path('api/v1/device/delete/<int:pk>', views.deleteDevice),
]