from django.urls import path
from device.views import device_return_views as views


urlpatterns = [
	path('api/v1/device_return/all/', views.getAllDeviceReturn),
	path('api/v1/get_all_company_device_return/', views.getAllDeviceReturnByCompany),

	path('api/v1/device_return/<int:pk>', views.getADeviceReturn),
	path('api/v1/get_company_device_return/<int:pk>', views.getADeviceReturnByCompany),

	path('api/v1/device_return/search/', views.searchDeviceReturn),
	path('api/v1/search_company_device_return/', views.searchDeviceReturnByCompany),

	path('api/v1/device_return/create/', views.createDeviceReturn),

	path('api/v1/device_return/update/<int:pk>', views.updateDeviceReturn),
	path('api/v1/update_company_device_return/<int:pk>', views.updateDeviceReturnByCompany),

	path('api/v1/device_return/delete/<int:pk>', views.deleteDeviceReturn),
	path('api/v1/delete_company_device_return/<int:pk>', views.deleteDeviceReturnByCompany),
]