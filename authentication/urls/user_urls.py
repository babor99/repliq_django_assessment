from authentication.views import user_views as views
from django.urls import path

urlpatterns = [

	path('api/v1/user/login/', views.MyTokenObtainPairView.as_view(), name='token_obtain_pair'),

	path('api/v1/user/all/', views.getAllUser),

	path('api/v1/user/without_pagination/all/', views.getAllUserWithoutPagination),

	path('api/v1/user/<int:pk>', views.getAUser),

	path('api/v1/user/me/', views.getMySelfUser),

	path('api/v1/user/verify/me/', views.verifyMySelfUser),

	path('api/v1/user/sign_up/', views.createUser),

	path('api/v1/user/update/<int:pk>', views.updateUser),

	path('api/v1/user/update/me/', views.updateMySelfUser),

	path('api/v1/user/delete/me/', views.deleteMySelfUser),

	path('api/v1/user/delete/<int:pk>', views.deleteUser),

	path('api/v1/user/passwordchange/<int:pk>', views.userPasswordChange),

	path('api/v1/user/uploadimage/<int:pk>', views.userImageUpload),

	path('api/v1/user/permission/', views.userHasPermission),

]
