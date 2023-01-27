from django.contrib import admin
from django.urls import path, include
from django.urls import include, path, re_path
from django.views.static import serve
from django.conf import settings

from drf_spectacular.views import (SpectacularAPIView, SpectacularRedocView, SpectacularSwaggerView)

from . import views




urlpatterns = [
    path('admin/', admin.site.urls),
    path('', views.index, name='index'),

    #authentication app
    path('role/', include('authentication.urls.role_urls')),
    path('permission/', include('authentication.urls.permission_urls')),
    path('user/', include('authentication.urls.user_urls')),
    path('employee/', include('authentication.urls.employee_urls')),

    #device app
    path('category/', include('device.urls.category_urls')),
    path('device/', include('device.urls.device_urls')),
    path('device_assign/', include('device.urls.device_assign_urls')),
    path('device_return/', include('device.urls.device_return_urls')),
    path('device_log/', include('device.urls.device_log_urls')),


    #swagger urls
    path('schema/', SpectacularAPIView.as_view(), name='schema'),
    path('schema/swagger-ui/', SpectacularSwaggerView.as_view(url_name='schema'), name='swagger-ui'),
    path('schema/redoc/', SpectacularRedocView.as_view(url_name='schema'), name='redoc'),

	re_path(r'^media/(?P<path>.*)$', serve,{'document_root': settings.MEDIA_ROOT}), 
    re_path(r'^static/(?P<path>.*)$', serve, {'document_root': settings.STATIC_ROOT}),

]
