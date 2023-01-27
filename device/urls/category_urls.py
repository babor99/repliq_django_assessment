from django.urls import path
from device.views import category_views as views


urlpatterns = [
	path('api/v1/all/', views.getAllCategory), # admin only
	path('api/v1/get_all_by_company/', views.getAllCategoryByCompany),

	path('api/v1/<int:pk>', views.getACategory), # admin only
	path('api/v1/get_company_category/<int:pk>', views.getACategoryByCompany),

	path('api/v1/search/', views.searchCategory), # admin only
	path('api/v1/company_category_search/', views.searchCategoryByCompany),

	path('api/v1/create/', views.createCategory),

	path('api/v1/update/<int:pk>', views.updateCategory), # admin only
	path('api/v1/company_category_update/<int:pk>', views.updateCategoryByCompany),

	path('api/v1/category/delete/<int:pk>', views.deleteCategory), # admin only
	path('api/v1/company_category_delete/<int:pk>', views.deleteCategoryByCompany),
]