from django.core.exceptions import ObjectDoesNotExist

from rest_framework import status
from rest_framework.decorators import api_view, permission_classes
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated

from drf_spectacular.utils import  extend_schema, OpenApiParameter

from authentication.decorators import IsAdminUser, has_permissions

from device.models import DeviceLog
from device.serializers import DeviceLogSerializer, DeviceLogListSerializer

from commons.pagination import Pagination




# Create your views here.

@extend_schema(
	parameters=[
		OpenApiParameter("page"),
		OpenApiParameter("size"),
  ],
	request=DeviceLogSerializer,
	responses=DeviceLogSerializer
)
@api_view(['GET'])
@permission_classes([IsAuthenticated, IsAdminUser])
# @has_permissions([PermissionEnum.PERMISSION_LIST_VIEW.name])
def getAllDeviceLog(request):
	device_logs = DeviceLog.objects.all()
	total_elements = device_logs.count()

	page = request.query_params.get('page')
	size = request.query_params.get('size')

	# Pagination
	pagination = Pagination()
	pagination.page = page
	pagination.size = size
	device_logs = pagination.paginate_data(device_logs)

	serializer = DeviceLogListSerializer(device_logs, many=True)

	response = {
		'device_logs': serializer.data,
		'page': pagination.page,
		'size': pagination.size,
		'total_pages': pagination.total_pages,
		'total_elements': total_elements,
	}

	return Response(response, status=status.HTTP_200_OK)




@extend_schema(
	request=DeviceLogSerializer,
	responses=DeviceLogSerializer
)
@api_view(['GET'])
@permission_classes([IsAuthenticated, IsAdminUser])
# @has_permissions([PermissionEnum.PERMISSION_LIST_VIEW.name])
def getAllDeviceLogWithoutPagination(request):
	device_logs = DeviceLog.objects.all()

	serializer = DeviceLogListSerializer(device_logs, many=True)

	return Response({'device_logs': serializer.data}, status=status.HTTP_200_OK)




@extend_schema(request=DeviceLogSerializer, responses=DeviceLogSerializer)
@api_view(['GET'])
@permission_classes([IsAuthenticated, IsAdminUser])
def getADeviceLog(request, pk):
	try:
		device_log = DeviceLog.objects.get(pk=pk)
		serializer = DeviceLogSerializer(device_log)
		return Response(serializer.data, status=status.HTTP_200_OK)
	except ObjectDoesNotExist:
		return Response({'detail': f"DeviceLog id - {pk} doesn't exists"}, status=status.HTTP_400_BAD_REQUEST)




@extend_schema(
	parameters=[
		OpenApiParameter('key'),
		OpenApiParameter('page'),
		OpenApiParameter('size'),
		],
	request=DeviceLogSerializer, 
	responses=DeviceLogSerializer)
@api_view(['GET'])
@permission_classes([IsAuthenticated, IsAdminUser])
# @has_permissions([PermissionEnum.PRODUCT_DETAILS.name])
def searchDeviceLog(request):
	key = request.query_params.get('key')
	device_logs = DeviceLog.objects.filter(name__icontains=key)

	total_elements = device_logs.count()

	page = request.query_params.get('page')
	size = request.query_params.get('size')

	# Pagination
	pagination = Pagination()
	pagination.page = page
	pagination.size = size
	device_logs = pagination.paginate_data(device_logs)

	serializer = DeviceLogListSerializer(device_logs, many=True)

	response = {
		'device_logs': serializer.data,
		'page': pagination.page,
		'size': pagination.size,
		'total_pages': pagination.total_pages,
		'total_elements': total_elements,
	}

	if len(device_logs) > 0:
		return Response(response, status=status.HTTP_200_OK)
	else:
		return Response({'detail': f"There are no device_logs matching your search"}, status=status.HTTP_204_NO_CONTENT)




@extend_schema(request=DeviceLogSerializer, responses=DeviceLogSerializer)
@api_view(['POST'])
@permission_classes([IsAuthenticated, IsAdminUser])
def createDeviceLog(request):
	data = request.data
	filtered_data = {}

	for key, value in data.items():
		if value != '' and value != 0 and value != '0':
			filtered_data[key] = value
			
	name = filtered_data.get('name', None)
	if name is not None:
		try:
			name = str(name).upper()
			device_log = DeviceLog.objects.get(name=name)
			return Response({'detail': f"DeviceLog with name '{name}' already exists."})
		except DeviceLog.DoesNotExist:
			pass

	serializer = DeviceLogSerializer(data=filtered_data)

	if serializer.is_valid():
		serializer.save()
		return Response(serializer.data, status=status.HTTP_201_CREATED)
	else:
		return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)




@extend_schema(request=DeviceLogSerializer, responses=DeviceLogSerializer)
@api_view(['PUT'])
@permission_classes([IsAuthenticated, IsAdminUser])
def updateDeviceLog(request,pk):
	data = request.data
	filtered_data = {}
	try:
		device_log = DeviceLog.objects.get(pk=pk)
	except ObjectDoesNotExist:
		return Response({'detail': f'device_log id - {pk} doesn\'t exists'}, status=status.HTTP_400_BAD_REQUEST)

	for key, value in data.items():
		if value != '' and value != 0 and value != '0':
			filtered_data[key] = value

	serializer = DeviceLogSerializer(device_log, data=filtered_data)
	if serializer.is_valid():
		serializer.save()
		return Response(serializer.data, status=status.HTTP_200_OK)
	else:
		return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)




@extend_schema(request=DeviceLogSerializer, responses=DeviceLogSerializer)
@api_view(['DELETE'])
@permission_classes([IsAuthenticated, IsAdminUser])
def deleteDeviceLog(request, pk):
	try:
		device_log = DeviceLog.objects.get(pk=pk)
		device_log.delete()
		return Response({'detail': f'DeviceLog id - {pk} is deleted successfully'}, status=status.HTTP_200_OK)
	except ObjectDoesNotExist:
		return Response({'detail': f"DeviceLog id - {pk} doesn't exists"}, status=status.HTTP_400_BAD_REQUEST)

