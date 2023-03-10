from django.urls import path
from authentication.views import employee_views as views


urlpatterns = [
	path('api/v1/employee/all/', views.getAllEmployee),
	path('api/v1/company_employee/all/', views.getAllEmployeeByCompany),

	path('api/v1/employee/<int:pk>', views.getAEmployee),
	path('api/v1/company_employee/<int:pk>', views.getAEmployeeByCompany),

	path('api/v1/employee/search/', views.searchEmployee),
	path('api/v1/search_company_employee/', views.searchEmployeeByCompany),

	path('api/v1/employee/create/', views.createEmployee),

	path('api/v1/employee/update/<int:pk>', views.updateEmployee),
	path('api/v1/update_company_employee/<int:pk>', views.updateEmployeeByCompany),

	path('api/v1/employee/delete/<int:pk>', views.deleteEmployee),
	path('api/v1/delete_company_employee/<int:pk>', views.deleteEmployeeByCompany),
]