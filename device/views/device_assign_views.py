from django.core.exceptions import ObjectDoesNotExist

from rest_framework import status
from rest_framework.decorators import api_view, permission_classes
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated

from drf_spectacular.utils import  extend_schema, OpenApiParameter

from authentication.decorators import IsAdminUser, has_permissions

from device.models import Device, DeviceAssign, DeviceLog
from device.serializers import DeviceAssignSerializer, DeviceAssignListSerializer

from commons.pagination import Pagination




# Create your views here.

@extend_schema(
	parameters=[
		OpenApiParameter("page"),
		OpenApiParameter("size"),
  ],
	request=DeviceAssignSerializer,
	responses=DeviceAssignSerializer
)
@api_view(['GET'])
@permission_classes([IsAuthenticated, IsAdminUser])
# @has_permissions([PermissionEnum.DEVICE_ASSIGN_DETAILS.name])
def getAllDeviceAssign(request):
	device_assigns = DeviceAssign.objects.all()
	total_elements = device_assigns.count()

	page = request.query_params.get('page')
	size = request.query_params.get('size')

	# Pagination
	pagination = Pagination()
	pagination.page = page
	pagination.size = size
	device_assigns = pagination.paginate_data(device_assigns)

	serializer = DeviceAssignListSerializer(device_assigns, many=True)

	response = {
		'device_assigns': serializer.data,
		'page': pagination.page,
		'size': pagination.size,
		'total_pages': pagination.total_pages,
		'total_elements': total_elements,
	}

	return Response(response, status=status.HTTP_200_OK)



# Create your views here.

@extend_schema(
	parameters=[
		OpenApiParameter("page"),
		OpenApiParameter("size"),
  ],
	request=DeviceAssignSerializer,
	responses=DeviceAssignSerializer
)
@api_view(['GET'])
@permission_classes([IsAuthenticated])
# @has_permissions([PermissionEnum.DEVICE_ASSIGN_DETAILS.name])
def getAllDeviceAssignByCompany(request):
	company = request.user
	device_assigns = DeviceAssign.objects.filter(company=company)
	total_elements = device_assigns.count()

	page = request.query_params.get('page')
	size = request.query_params.get('size')

	# Pagination
	pagination = Pagination()
	pagination.page = page
	pagination.size = size
	device_assigns = pagination.paginate_data(device_assigns)

	serializer = DeviceAssignListSerializer(device_assigns, many=True)

	response = {
		'device_assigns': serializer.data,
		'page': pagination.page,
		'size': pagination.size,
		'total_pages': pagination.total_pages,
		'total_elements': total_elements,
	}

	return Response(response, status=status.HTTP_200_OK)




@extend_schema(request=DeviceAssignSerializer, responses=DeviceAssignSerializer)
@api_view(['GET'])
@permission_classes([IsAuthenticated, IsAdminUser])
# @has_permissions([PermissionEnum.DEVICE_ASSIGN_DETAILS.name])
def getADeviceAssign(request, pk):
	try:
		device_assign = DeviceAssign.objects.get(pk=pk)
		serializer = DeviceAssignSerializer(device_assign)
		return Response(serializer.data, status=status.HTTP_200_OK)
	except ObjectDoesNotExist:
		return Response({'detail': f"DeviceAssign id - {pk} doesn't exists"}, status=status.HTTP_400_BAD_REQUEST)





@extend_schema(request=DeviceAssignSerializer, responses=DeviceAssignSerializer)
@api_view(['GET'])
@permission_classes([IsAuthenticated, IsAdminUser])
# @has_permissions([PermissionEnum.DEVICE_ASSIGN_DETAILS.name])
def getADeviceAssignByCompany(request, pk):
	company = request.user
	try:
		device_assign = DeviceAssign.objects.get(pk=pk, company=company)
		serializer = DeviceAssignSerializer(device_assign)
		return Response(serializer.data, status=status.HTTP_200_OK)
	except ObjectDoesNotExist:
		return Response({'detail': f"DeviceAssign id - {pk} doesn't exists"}, status=status.HTTP_400_BAD_REQUEST)




@extend_schema(
	parameters=[
		OpenApiParameter('key'),
		OpenApiParameter('page'),
		OpenApiParameter('size'),
		],
	request=DeviceAssignSerializer, 
	responses=DeviceAssignSerializer)
@api_view(['GET'])
@permission_classes([IsAuthenticated, IsAdminUser])
# @has_permissions([PermissionEnum.DEVICE_ASSIGN_DETAILS.name])
def searchDeviceAssign(request):
	key = request.query_params.get('key')
	device_assigns = DeviceAssign.objects.filter(ddevice__name__icontainsevice__id=key)

	total_elements = device_assigns.count()

	page = request.query_params.get('page')
	size = request.query_params.get('size')

	# Pagination
	pagination = Pagination()
	pagination.page = page
	pagination.size = size
	device_assigns = pagination.paginate_data(device_assigns)

	serializer = DeviceAssignListSerializer(device_assigns, many=True)

	response = {
		'device_assigns': serializer.data,
		'page': pagination.page,
		'size': pagination.size,
		'total_pages': pagination.total_pages,
		'total_elements': total_elements,
	}

	if len(device_assigns) > 0:
		return Response(response, status=status.HTTP_200_OK)
	else:
		return Response({'detail': f"There are no device_assigns matching your search"}, status=status.HTTP_204_NO_CONTENT)




@extend_schema(
	parameters=[
		OpenApiParameter('key'),
		OpenApiParameter('page'),
		OpenApiParameter('size'),
		],
	request=DeviceAssignSerializer, 
	responses=DeviceAssignSerializer)
@api_view(['GET'])
@permission_classes([IsAuthenticated])
# @has_permissions([PermissionEnum.DEVICE_ASSIGN_DETAILS.name])
def searchDeviceAssignByCompany(request):
	company = request.user
	key = request.query_params.get('key')
	device_assigns = DeviceAssign.objects.filter(device__name__icontains=key, company=company)

	total_elements = device_assigns.count()

	page = request.query_params.get('page')
	size = request.query_params.get('size')

	# Pagination
	pagination = Pagination()
	pagination.page = page
	pagination.size = size
	device_assigns = pagination.paginate_data(device_assigns)

	serializer = DeviceAssignListSerializer(device_assigns, many=True)

	response = {
		'device_assigns': serializer.data,
		'page': pagination.page,
		'size': pagination.size,
		'total_pages': pagination.total_pages,
		'total_elements': total_elements,
	}

	if len(device_assigns) > 0:
		return Response(response, status=status.HTTP_200_OK)
	else:
		return Response({'detail': f"There are no device_assigns matching your search"}, status=status.HTTP_204_NO_CONTENT)




@extend_schema(request=DeviceAssignSerializer, responses=DeviceAssignSerializer)
@api_view(['POST'])
@permission_classes([IsAuthenticated, IsAdminUser])
# @has_permissions([PermissionEnum.DEVICE_ASSIGN_DETAILS.name])
def createDeviceAssign(request):
	company = request.user
	data = request.data
	filtered_data = {}

	for key, value in data.items():
		if value != '' and value != 0 and value != '0':
			filtered_data[key] = value

	serializer = DeviceAssignSerializer(data=filtered_data)

	if serializer.is_valid():
		try:
			device = Device.objects.get(pk=filtered_data['device'])
			DeviceLog.objects.create(type="assign", device=device, company=company, description=filtered_data.get('condition',''))
		except:
			pass
		serializer.save()
		return Response(serializer.data, status=status.HTTP_201_CREATED)
	else:
		return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)




@extend_schema(request=DeviceAssignSerializer, responses=DeviceAssignSerializer)
@api_view(['PUT'])
@permission_classes([IsAuthenticated, IsAdminUser])
# @has_permissions([PermissionEnum.DEVICE_ASSIGN_DETAILS.name])
def updateDeviceAssign(request, pk):
	data = request.data
	filtered_data = {}
	try:
		device_assign = DeviceAssign.objects.get(pk=pk)
	except ObjectDoesNotExist:
		return Response({'detail': f'device_assign id - {pk} doesn\'t exists'}, status=status.HTTP_400_BAD_REQUEST)

	for key, value in data.items():
		if value != '' and value != 0 and value != '0':
			filtered_data[key] = value

	serializer = DeviceAssignSerializer(device_assign, data=filtered_data)
	if serializer.is_valid():
		serializer.save()
		return Response(serializer.data, status=status.HTTP_200_OK)
	else:
		return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)




@extend_schema(request=DeviceAssignSerializer, responses=DeviceAssignSerializer)
@api_view(['PUT'])
@permission_classes([IsAuthenticated])
# @has_permissions([PermissionEnum.DEVICE_ASSIGN_DETAILS.name])
def updateDeviceAssignByCompany(request, pk):
	company = request.user
	data = request.data
	filtered_data = {}
	try:
		device_assign = DeviceAssign.objects.get(pk=pk, company=company)
	except ObjectDoesNotExist:
		return Response({'detail': f'device_assign id - {pk} doesn\'t exists'}, status=status.HTTP_400_BAD_REQUEST)

	for key, value in data.items():
		if value != '' and value != 0 and value != '0':
			filtered_data[key] = value

	serializer = DeviceAssignSerializer(device_assign, data=filtered_data)
	if serializer.is_valid():
		serializer.save()
		return Response(serializer.data, status=status.HTTP_200_OK)
	else:
		return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)




@extend_schema(request=DeviceAssignSerializer, responses=DeviceAssignSerializer)
@api_view(['DELETE'])
@permission_classes([IsAuthenticated, IsAdminUser])
# @has_permissions([PermissionEnum.DEVICE_ASSIGN_DETAILS.name])
def deleteDeviceAssign(request, pk):
	try:
		device_assign = DeviceAssign.objects.get(pk=pk)
		device_assign.delete()
		return Response({'detail': f'DeviceAssign id - {pk} is deleted successfully'}, status=status.HTTP_200_OK)
	except ObjectDoesNotExist:
		return Response({'detail': f"DeviceAssign id - {pk} doesn't exists"}, status=status.HTTP_400_BAD_REQUEST)




@extend_schema(request=DeviceAssignSerializer, responses=DeviceAssignSerializer)
@api_view(['DELETE'])
@permission_classes([IsAuthenticated])
# @has_permissions([PermissionEnum.DEVICE_ASSIGN_DETAILS.name])
def deleteDeviceAssignByCompany(request, pk):
	company = request.user
	try:
		device_assign = DeviceAssign.objects.get(pk=pk, company=company)
		device_assign.delete()
		return Response({'detail': f'DeviceAssign id - {pk} is deleted successfully'}, status=status.HTTP_200_OK)
	except ObjectDoesNotExist:
		return Response({'detail': f"DeviceAssign id - {pk} doesn't exists"}, status=status.HTTP_400_BAD_REQUEST)

