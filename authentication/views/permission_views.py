from django.core.exceptions import ObjectDoesNotExist

from rest_framework import status
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response

from drf_spectacular.utils import  extend_schema, OpenApiParameter

from authentication.decorators import IsAdminUser, has_permissions
from authentication.models import Permission
from authentication.serializers import PermissionSerializer, PermissionListSerializer

from commons.enums import PermissionEnum
from commons.pagination import Pagination




# Create your views here.

@extend_schema(
	parameters=[
		OpenApiParameter("page"),
		OpenApiParameter("size"),
  ],
	request=PermissionSerializer,
	responses=PermissionSerializer
)
@api_view(['GET'])
@permission_classes([IsAuthenticated, IsAdminUser])
# @has_permissions([PermissionEnum.PERMISSION_LIST.name])
def getAllPermission(request):
	permissions = Permission.objects.all()
	total_elements = permissions.count()

	page = request.query_params.get('page')
	size = request.query_params.get('size')

	# Pagination
	pagination = Pagination()
	pagination.page = page
	pagination.size = size
	permissions = pagination.paginate_data(permissions)

	serializer = PermissionListSerializer(permissions, many=True)

	response = {
		'permissions': serializer.data,
		'page': pagination.page,
		'size': pagination.size,
		'total_pages': pagination.total_pages,
		'total_elements': total_elements,
	}

	return Response(response, status=status.HTTP_200_OK)




@extend_schema(
	request=PermissionSerializer,
	responses=PermissionSerializer
)
@api_view(['GET'])
@permission_classes([IsAuthenticated, IsAdminUser])
# @has_permissions([PermissionEnum.PERMISSION_LIST.name])
def getAllPermissionWithoutPagination(request):
	permissions = Permission.objects.all()

	serializer = PermissionListSerializer(permissions, many=True)

	return Response({'permissions': serializer.data}, status=status.HTTP_200_OK)




@extend_schema(request=PermissionSerializer, responses=PermissionSerializer)
@api_view(['GET'])
@permission_classes([IsAuthenticated, IsAdminUser])
# @has_permissions([PermissionEnum.PERMISSION_DETAILS.name])
def getAPermission(request, pk):
	try:
		permission = Permission.objects.get(pk=pk)
		serializer = PermissionSerializer(permission)
		return Response(serializer.data, status=status.HTTP_200_OK)
	except ObjectDoesNotExist:
		return Response({'detail': f"Permission id - {pk} doesn't exists"}, status=status.HTTP_400_BAD_REQUEST)




@extend_schema(
	parameters=[
		OpenApiParameter('key'),
		OpenApiParameter('page'),
		OpenApiParameter('size'),
		],
	request=PermissionSerializer, 
	responses=PermissionSerializer)
@api_view(['GET'])
@permission_classes([IsAuthenticated, IsAdminUser])
# @has_permissions([PermissionEnum.PRODUCT_DETAILS.name])
def searchPermission (request):
	key = request.query_params.get('key')
	permissions = Permission.objects.filter(name__icontains=key)

	total_elements = permissions.count()

	page = request.query_params.get('page')
	size = request.query_params.get('size')

	# Pagination
	pagination = Pagination()
	pagination.page = page
	pagination.size = size
	permissions = pagination.paginate_data(permissions)

	serializer = PermissionListSerializer(permissions, many=True)

	response = {
		'permissions': serializer.data,
		'page': pagination.page,
		'size': pagination.size,
		'total_pages': pagination.total_pages,
		'total_elements': total_elements,
	}

	if len(permissions) > 0:
		return Response(response, status=status.HTTP_200_OK)
	else:
		return Response({'detail': f"There are no permissions matching your search"}, status=status.HTTP_204_NO_CONTENT)




@extend_schema(request=PermissionSerializer, responses=PermissionSerializer)
@api_view(['POST'])
@permission_classes([IsAuthenticated, IsAdminUser])
# @has_permissions([PermissionEnum.PERMISSION_CREATE.name])
def createPermission(request):
	data = request.data
	filtered_data = {}

	for key, value in data.items():
		if value != '' and value != 0 and value != '0':
			filtered_data[key] = value

	name = filtered_data.get('name', None)
	if name is not None:
		try:
			name = str(name).upper()
			role = Permission.objects.get(name=name)
			return Response({'detail': f"Permission with name '{name}' already exists."})
		except Permission.DoesNotExist:
			pass

	serializer = PermissionSerializer(data=filtered_data)

	if serializer.is_valid():
		serializer.save()
		return Response(serializer.data, status=status.HTTP_201_CREATED)
	else:
		return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)




@extend_schema(request=PermissionSerializer, responses=PermissionSerializer)
@api_view(['PUT'])
@permission_classes([IsAuthenticated, IsAdminUser])
# @has_permissions([PermissionEnum.PERMISSION_UPDATE.name])
def updatePermission(request,pk):
	data = request.data
	filtered_data = {}

	for key, value in data.items():
		if value != '' and value != 0 and value != '0':
			filtered_data[key] = value

	try:
		permission = Permission.objects.get(pk=pk)
	except ObjectDoesNotExist:
		return Response({'detail': f'permission id - {pk} doesn\'t exists'}, status=status.HTTP_400_BAD_REQUEST)

	serializer = PermissionSerializer(permission, data=filtered_data)
	if serializer.is_valid():
		serializer.save()
		return Response(serializer.data, status=status.HTTP_200_OK)
	else:
		return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)




@extend_schema(request=PermissionSerializer, responses=PermissionSerializer)
@api_view(['DELETE'])
@permission_classes([IsAuthenticated, IsAdminUser])
# @has_permissions([PermissionEnum.PERMISSION_DELETE.name])
def deletePermission(request, pk):
	try:
		permission = Permission.objects.get(pk=pk)
		permission.delete()
		return Response({'detail': f'Permission id - {pk} is deleted successfully'}, status=status.HTTP_200_OK)
	except ObjectDoesNotExist:
		return Response({'detail': f"Permission id - {pk} doesn't exists"}, status=status.HTTP_400_BAD_REQUEST)



