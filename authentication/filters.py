from authentication.models import *
from django_filters import rest_framework as filters




class UserFilter(filters.FilterSet):
    username = filters.CharFilter(field_name="username", lookup_expr='icontains')

    class Meta:
        model = User
        fields = ['username', ]




class RoleFilter(filters.FilterSet):
    name = filters.CharFilter(field_name="name", lookup_expr='icontains')

    class Meta:
        model = Role
        fields = ['name', ]




class PermissionFilter(filters.FilterSet):
    name = filters.CharFilter(field_name="name", lookup_expr='icontains')

    class Meta:
        model = Permission
        fields = ['name', ]


