from django.core.exceptions import ObjectDoesNotExist

from rest_framework import status
from rest_framework.decorators import api_view, permission_classes
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated

from drf_spectacular.utils import  extend_schema, OpenApiParameter

from authentication.decorators import IsAdminUser, has_permissions

from device.models import Device, DeviceLog, DeviceReturn
from device.serializers import DeviceReturnSerializer, DeviceReturnListSerializer

from commons.pagination import Pagination




# Create your views here.

@extend_schema(
	parameters=[
		OpenApiParameter("page"),
		OpenApiParameter("size"),
  ],
	request=DeviceReturnSerializer,
	responses=DeviceReturnSerializer
)
@api_view(['GET'])
@permission_classes([IsAuthenticated, IsAdminUser])
# @has_permissions([PermissionEnum.DEVICE_RETURN_DETAILS.name])
def getAllDeviceReturn(request):
	device_returns = DeviceReturn.objects.all()
	total_elements = device_returns.count()

	page = request.query_params.get('page')
	size = request.query_params.get('size')

	# Pagination
	pagination = Pagination()
	pagination.page = page
	pagination.size = size
	device_returns = pagination.paginate_data(device_returns)

	serializer = DeviceReturnListSerializer(device_returns, many=True)

	response = {
		'device_returns': serializer.data,
		'page': pagination.page,
		'size': pagination.size,
		'total_pages': pagination.total_pages,
		'total_elements': total_elements,
	}

	return Response(response, status=status.HTTP_200_OK)




@extend_schema(
	parameters=[
		OpenApiParameter("page"),
		OpenApiParameter("size"),
  ],
	request=DeviceReturnSerializer,
	responses=DeviceReturnSerializer
)
@api_view(['GET'])
@permission_classes([IsAuthenticated])
# @has_permissions([PermissionEnum.DEVICE_RETURN_DETAILS.name])
def getAllDeviceReturnByCompany(request):
	company = request.user
	device_returns = DeviceReturn.objects.filter(company=company)
	total_elements = device_returns.count()

	page = request.query_params.get('page')
	size = request.query_params.get('size')

	# Pagination
	pagination = Pagination()
	pagination.page = page
	pagination.size = size
	device_returns = pagination.paginate_data(device_returns)

	serializer = DeviceReturnListSerializer(device_returns, many=True)

	response = {
		'device_returns': serializer.data,
		'page': pagination.page,
		'size': pagination.size,
		'total_pages': pagination.total_pages,
		'total_elements': total_elements,
	}

	return Response(response, status=status.HTTP_200_OK)




@extend_schema(request=DeviceReturnSerializer, responses=DeviceReturnSerializer)
@api_view(['GET'])
@permission_classes([IsAuthenticated, IsAdminUser])
# @has_permissions([PermissionEnum.DEVICE_RETURN_DETAILS.name])
def getADeviceReturn(request, pk):
	try:
		device_return = DeviceReturn.objects.get(pk=pk)
		serializer = DeviceReturnSerializer(device_return)
		return Response(serializer.data, status=status.HTTP_200_OK)
	except ObjectDoesNotExist:
		return Response({'detail': f"DeviceReturn id - {pk} doesn't exists"}, status=status.HTTP_400_BAD_REQUEST)




@extend_schema(request=DeviceReturnSerializer, responses=DeviceReturnSerializer)
@api_view(['GET'])
@permission_classes([IsAuthenticated])
# @has_permissions([PermissionEnum.DEVICE_RETURN_DETAILS.name])
def getADeviceReturnByCompany(request, pk):
	company = request.user
	try:
		device_return = DeviceReturn.objects.get(pk=pk, company=company)
		serializer = DeviceReturnSerializer(device_return)
		return Response(serializer.data, status=status.HTTP_200_OK)
	except ObjectDoesNotExist:
		return Response({'detail': f"DeviceReturn id - {pk} doesn't exists"}, status=status.HTTP_400_BAD_REQUEST)




@extend_schema(
	parameters=[
		OpenApiParameter('key'),
		OpenApiParameter('page'),
		OpenApiParameter('size'),
		],
	request=DeviceReturnSerializer, 
	responses=DeviceReturnSerializer)
@api_view(['GET'])
@permission_classes([IsAuthenticated, IsAdminUser])
# @has_permissions([PermissionEnum.DEVICE_RETURN_DETAILS.name])
def searchDeviceReturn(request):
	key = request.query_params.get('key')
	device_returns = DeviceReturn.objects.filter(device__name__icontains=key)

	total_elements = device_returns.count()

	page = request.query_params.get('page')
	size = request.query_params.get('size')

	# Pagination
	pagination = Pagination()
	pagination.page = page
	pagination.size = size
	device_returns = pagination.paginate_data(device_returns)

	serializer = DeviceReturnListSerializer(device_returns, many=True)

	response = {
		'device_returns': serializer.data,
		'page': pagination.page,
		'size': pagination.size,
		'total_pages': pagination.total_pages,
		'total_elements': total_elements,
	}

	if len(device_returns) > 0:
		return Response(response, status=status.HTTP_200_OK)
	else:
		return Response({'detail': f"There are no device_returns matching your search"}, status=status.HTTP_204_NO_CONTENT)




@extend_schema(
	parameters=[
		OpenApiParameter('key'),
		OpenApiParameter('page'),
		OpenApiParameter('size'),
		],
	request=DeviceReturnSerializer, 
	responses=DeviceReturnSerializer)
@api_view(['GET'])
@permission_classes([IsAuthenticated])
# @has_permissions([PermissionEnum.DEVICE_RETURN_DETAILS.name])
def searchDeviceReturnByCompany(request):
	company = request.user
	key = request.query_params.get('key')
	device_returns = DeviceReturn.objects.filter(device__name__icontains=key, company=company)

	total_elements = device_returns.count()

	page = request.query_params.get('page')
	size = request.query_params.get('size')

	# Pagination
	pagination = Pagination()
	pagination.page = page
	pagination.size = size
	device_returns = pagination.paginate_data(device_returns)

	serializer = DeviceReturnListSerializer(device_returns, many=True)

	response = {
		'device_returns': serializer.data,
		'page': pagination.page,
		'size': pagination.size,
		'total_pages': pagination.total_pages,
		'total_elements': total_elements,
	}

	if len(device_returns) > 0:
		return Response(response, status=status.HTTP_200_OK)
	else:
		return Response({'detail': f"There are no device_returns matching your search"}, status=status.HTTP_204_NO_CONTENT)




@extend_schema(request=DeviceReturnSerializer, responses=DeviceReturnSerializer)
@api_view(['POST'])
@permission_classes([IsAuthenticated, IsAdminUser])
# @has_permissions([PermissionEnum.DEVICE_RETURN_DETAILS.name])
def createDeviceReturn(request):
	company= request.user
	data = request.data
	filtered_data = {}

	for key, value in data.items():
		if value != '' and value != 0 and value != '0':
			filtered_data[key] = value
			

	serializer = DeviceReturnSerializer(data=filtered_data)

	if serializer.is_valid():
		try:
			device = Device.objects.get(pk=filtered_data['device'])
			DeviceLog.objects.create(type="return", device=device, company=company, description=filtered_data.get('condition',''))
		except:
			pass
		serializer.save()
		return Response(serializer.data, status=status.HTTP_201_CREATED)
	else:
		return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)




@extend_schema(request=DeviceReturnSerializer, responses=DeviceReturnSerializer)
@api_view(['PUT'])
@permission_classes([IsAuthenticated, IsAdminUser])
# @has_permissions([PermissionEnum.DEVICE_RETURN_DETAILS.name])
def updateDeviceReturn(request,pk):
	data = request.data
	filtered_data = {}
	try:
		device_return = DeviceReturn.objects.get(pk=pk)
	except ObjectDoesNotExist:
		return Response({'detail': f'device_return id - {pk} doesn\'t exists'}, status=status.HTTP_400_BAD_REQUEST)

	for key, value in data.items():
		if value != '' and value != 0 and value != '0':
			filtered_data[key] = value

	serializer = DeviceReturnSerializer(device_return, data=filtered_data)
	if serializer.is_valid():
		serializer.save()
		return Response(serializer.data, status=status.HTTP_200_OK)
	else:
		return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)




@extend_schema(request=DeviceReturnSerializer, responses=DeviceReturnSerializer)
@api_view(['PUT'])
@permission_classes([IsAuthenticated])
# @has_permissions([PermissionEnum.DEVICE_RETURN_DETAILS.name])
def updateDeviceReturnByCompany(request,pk):
	company = request.user
	data = request.data
	filtered_data = {}
	try:
		device_return = DeviceReturn.objects.get(pk=pk, company=company)
	except ObjectDoesNotExist:
		return Response({'detail': f'device_return id - {pk} doesn\'t exists'}, status=status.HTTP_400_BAD_REQUEST)

	for key, value in data.items():
		if value != '' and value != 0 and value != '0':
			filtered_data[key] = value

	serializer = DeviceReturnSerializer(device_return, data=filtered_data)
	if serializer.is_valid():
		serializer.save()
		return Response(serializer.data, status=status.HTTP_200_OK)
	else:
		return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)




@extend_schema(request=DeviceReturnSerializer, responses=DeviceReturnSerializer)
@api_view(['DELETE'])
@permission_classes([IsAuthenticated, IsAdminUser])
# @has_permissions([PermissionEnum.DEVICE_RETURN_DETAILS.name])
def deleteDeviceReturn(request, pk):
	try:
		device_return = DeviceReturn.objects.get(pk=pk)
		device_return.delete()
		return Response({'detail': f'DeviceReturn id - {pk} is deleted successfully'}, status=status.HTTP_200_OK)
	except ObjectDoesNotExist:
		return Response({'detail': f"DeviceReturn id - {pk} doesn't exists"}, status=status.HTTP_400_BAD_REQUEST)




@extend_schema(request=DeviceReturnSerializer, responses=DeviceReturnSerializer)
@api_view(['DELETE'])
@permission_classes([IsAuthenticated])
# @has_permissions([PermissionEnum.DEVICE_RETURN_DETAILS.name])
def deleteDeviceReturnByCompany(request, pk):
	company = request.user
	try:
		device_return = DeviceReturn.objects.get(pk=pk, company=company)
		device_return.delete()
		return Response({'detail': f'DeviceReturn id - {pk} is deleted successfully'}, status=status.HTTP_200_OK)
	except ObjectDoesNotExist:
		return Response({'detail': f"DeviceReturn id - {pk} doesn't exists"}, status=status.HTTP_400_BAD_REQUEST)

