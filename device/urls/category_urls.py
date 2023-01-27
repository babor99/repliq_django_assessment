from django.urls import path
from device.views import category_views as views


urlpatterns = [
	path('api/v1/category/all/', views.getAllCategory),

	path('api/v1/category/without_pagination/all/', views.getAllCategoryWithoutPagination),

	path('api/v1/category/<int:pk>', views.getACategory),

	path('api/v1/category/search/', views.searchCategory),

	path('api/v1/category/create/', views.createCategory),

	path('api/v1/category/update/<int:pk>', views.updateCategory),

	path('api/v1/category/delete/<int:pk>', views.deleteCategory),
]