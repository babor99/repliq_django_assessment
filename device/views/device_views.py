from django.core.exceptions import ObjectDoesNotExist

from rest_framework import status
from rest_framework.decorators import api_view, permission_classes
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated

from drf_spectacular.utils import  extend_schema, OpenApiParameter

from authentication.decorators import IsAdminUser, has_permissions

from device.models import Device
from device.serializers import DeviceSerializer, DeviceListSerializer

from commons.pagination import Pagination




# Create your views here.

@extend_schema(
	parameters=[
		OpenApiParameter("page"),
		OpenApiParameter("size"),
  ],
	request=DeviceSerializer,
	responses=DeviceSerializer
)
@api_view(['GET'])
@permission_classes([IsAuthenticated, IsAdminUser])
# @has_permissions([PermissionEnum.PERMISSION_LIST_VIEW.name])
def getAllDevice(request):
	devices = Device.objects.all()
	total_elements = devices.count()

	page = request.query_params.get('page')
	size = request.query_params.get('size')

	# Pagination
	pagination = Pagination()
	pagination.page = page
	pagination.size = size
	devices = pagination.paginate_data(devices)

	serializer = DeviceListSerializer(devices, many=True)

	response = {
		'devices': serializer.data,
		'page': pagination.page,
		'size': pagination.size,
		'total_pages': pagination.total_pages,
		'total_elements': total_elements,
	}

	return Response(response, status=status.HTTP_200_OK)




@extend_schema(
	request=DeviceSerializer,
	responses=DeviceSerializer
)
@api_view(['GET'])
@permission_classes([IsAuthenticated, IsAdminUser])
# @has_permissions([PermissionEnum.PERMISSION_LIST_VIEW.name])
def getAllDeviceWithoutPagination(request):
	devices = Device.objects.all()

	serializer = DeviceListSerializer(devices, many=True)

	return Response({'devices': serializer.data}, status=status.HTTP_200_OK)




@extend_schema(request=DeviceSerializer, responses=DeviceSerializer)
@api_view(['GET'])
@permission_classes([IsAuthenticated, IsAdminUser])
def getADevice(request, pk):
	try:
		device = Device.objects.get(pk=pk)
		serializer = DeviceSerializer(device)
		return Response(serializer.data, status=status.HTTP_200_OK)
	except ObjectDoesNotExist:
		return Response({'detail': f"Device id - {pk} doesn't exists"}, status=status.HTTP_400_BAD_REQUEST)




@extend_schema(
	parameters=[
		OpenApiParameter('key'),
		OpenApiParameter('page'),
		OpenApiParameter('size'),
		],
	request=DeviceSerializer, 
	responses=DeviceSerializer)
@api_view(['GET'])
@permission_classes([IsAuthenticated, IsAdminUser])
# @has_permissions([PermissionEnum.PRODUCT_DETAILS.name])
def searchDevice(request):
	key = request.query_params.get('key')
	devices = Device.objects.filter(name__icontains=key)

	total_elements = devices.count()

	page = request.query_params.get('page')
	size = request.query_params.get('size')

	# Pagination
	pagination = Pagination()
	pagination.page = page
	pagination.size = size
	devices = pagination.paginate_data(devices)

	serializer = DeviceListSerializer(devices, many=True)

	response = {
		'devices': serializer.data,
		'page': pagination.page,
		'size': pagination.size,
		'total_pages': pagination.total_pages,
		'total_elements': total_elements,
	}

	if len(devices) > 0:
		return Response(response, status=status.HTTP_200_OK)
	else:
		return Response({'detail': f"There are no devices matching your search"}, status=status.HTTP_204_NO_CONTENT)




@extend_schema(request=DeviceSerializer, responses=DeviceSerializer)
@api_view(['POST'])
@permission_classes([IsAuthenticated, IsAdminUser])
def createDevice(request):
	data = request.data
	filtered_data = {}

	for key, value in data.items():
		if value != '' and value != 0 and value != '0':
			filtered_data[key] = value
			
	name = filtered_data.get('name', None)
	if name is not None:
		try:
			name = str(name).upper()
			device = Device.objects.get(name=name)
			return Response({'detail': f"Device with name '{name}' already exists."})
		except Device.DoesNotExist:
			pass

	serializer = DeviceSerializer(data=filtered_data)

	if serializer.is_valid():
		serializer.save()
		return Response(serializer.data, status=status.HTTP_201_CREATED)
	else:
		return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)




@extend_schema(request=DeviceSerializer, responses=DeviceSerializer)
@api_view(['PUT'])
@permission_classes([IsAuthenticated, IsAdminUser])
def updateDevice(request,pk):
	data = request.data
	filtered_data = {}
	try:
		device = Device.objects.get(pk=pk)
	except ObjectDoesNotExist:
		return Response({'detail': f'device id - {pk} doesn\'t exists'}, status=status.HTTP_400_BAD_REQUEST)

	for key, value in data.items():
		if value != '' and value != 0 and value != '0':
			filtered_data[key] = value

	serializer = DeviceSerializer(device, data=filtered_data)
	if serializer.is_valid():
		serializer.save()
		return Response(serializer.data, status=status.HTTP_200_OK)
	else:
		return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)




@extend_schema(request=DeviceSerializer, responses=DeviceSerializer)
@api_view(['DELETE'])
@permission_classes([IsAuthenticated, IsAdminUser])
def deleteDevice(request, pk):
	try:
		device = Device.objects.get(pk=pk)
		device.delete()
		return Response({'detail': f'Device id - {pk} is deleted successfully'}, status=status.HTTP_200_OK)
	except ObjectDoesNotExist:
		return Response({'detail': f"Device id - {pk} doesn't exists"}, status=status.HTTP_400_BAD_REQUEST)

