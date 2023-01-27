from django.urls import path
from authentication.views import employee_views as views


urlpatterns = [
	path('api/v1/employee/all/', views.getAllEmployee),

	path('api/v1/employee/without_pagination/all/', views.getAllEmployeeWithoutPagination),

	path('api/v1/employee/<int:pk>', views.getAEmployee),

	path('api/v1/employee/search/', views.searchEmployee),

	path('api/v1/employee/create/', views.createEmployee),

	path('api/v1/employee/update/<int:pk>', views.updateEmployee),

	path('api/v1/employee/delete/<int:pk>', views.deleteEmployee),
]