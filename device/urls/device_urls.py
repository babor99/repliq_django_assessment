from django.urls import path
from device.views import device_views as views


urlpatterns = [
	path('api/v1/all/', views.getAllDevice), # admin only
	path('api/v1/get_all_company_device/', views.getAllDeviceByCompany),

	path('api/v1/<int:pk>', views.getADevice), # admin only
	path('api/v1/get_company_device/<int:pk>', views.getADeviceByCompany),

	path('api/v1/search/', views.searchDevice), # admin only
	path('api/v1/company_device_search/', views.searchDeviceByCompany),

	path('api/v1/create/', views.createDevice),

	path('api/v1/update/<int:pk>', views.updateDevice), # admin only
	path('api/v1/company_device_update/<int:pk>', views.updateDeviceByCompany),

	path('api/v1/delete/<int:pk>', views.deleteDevice), # admin only
	path('api/v1/company_device_delete/<int:pk>', views.deleteDeviceByCompany),
]