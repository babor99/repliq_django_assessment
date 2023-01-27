from django.core.exceptions import ObjectDoesNotExist

from rest_framework import status
from rest_framework.decorators import api_view, permission_classes
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated

from drf_spectacular.utils import  extend_schema, OpenApiParameter

from authentication.decorators import IsAdminUser, has_permissions
from authentication.models import Employee
from authentication.serializers import EmployeeSerializer, EmployeeListSerializer

from commons.pagination import Pagination




# Create your views here.

@extend_schema(
	parameters=[
		OpenApiParameter("page"),
		OpenApiParameter("size"),
  ],
	request=EmployeeSerializer,
	responses=EmployeeSerializer
)
@api_view(['GET'])
@permission_classes([IsAuthenticated, IsAdminUser])
# @has_permissions([PermissionEnum.PERMISSION_LIST_VIEW.name])
def getAllEmployee(request):
	employees = Employee.objects.all()
	total_elements = employees.count()

	page = request.query_params.get('page')
	size = request.query_params.get('size')

	# Pagination
	pagination = Pagination()
	pagination.page = page
	pagination.size = size
	employees = pagination.paginate_data(employees)

	serializer = EmployeeListSerializer(employees, many=True)

	response = {
		'employees': serializer.data,
		'page': pagination.page,
		'size': pagination.size,
		'total_pages': pagination.total_pages,
		'total_elements': total_elements,
	}

	return Response(response, status=status.HTTP_200_OK)




@extend_schema(
	request=EmployeeSerializer,
	responses=EmployeeSerializer
)
@api_view(['GET'])
@permission_classes([IsAuthenticated, IsAdminUser])
# @has_permissions([PermissionEnum.PERMISSION_LIST_VIEW.name])
def getAllEmployeeWithoutPagination(request):
	employees = Employee.objects.all()

	serializer = EmployeeListSerializer(employees, many=True)

	return Response({'employees': serializer.data}, status=status.HTTP_200_OK)




@extend_schema(request=EmployeeSerializer, responses=EmployeeSerializer)
@api_view(['GET'])
@permission_classes([IsAuthenticated, IsAdminUser])
def getAEmployee(request, pk):
	try:
		employee = Employee.objects.get(pk=pk)
		serializer = EmployeeSerializer(employee)
		return Response(serializer.data, status=status.HTTP_200_OK)
	except ObjectDoesNotExist:
		return Response({'detail': f"Employee id - {pk} doesn't exists"}, status=status.HTTP_400_BAD_REQUEST)




@extend_schema(
	parameters=[
		OpenApiParameter('key'),
		OpenApiParameter('page'),
		OpenApiParameter('size'),
		],
	request=EmployeeSerializer, 
	responses=EmployeeSerializer)
@api_view(['GET'])
@permission_classes([IsAuthenticated, IsAdminUser])
# @has_permissions([PermissionEnum.PRODUCT_DETAILS.name])
def searchEmployee(request):
	key = request.query_params.get('key')
	employees = Employee.objects.filter(name__icontains=key)

	total_elements = employees.count()

	page = request.query_params.get('page')
	size = request.query_params.get('size')

	# Pagination
	pagination = Pagination()
	pagination.page = page
	pagination.size = size
	employees = pagination.paginate_data(employees)

	serializer = EmployeeListSerializer(employees, many=True)

	response = {
		'employees': serializer.data,
		'page': pagination.page,
		'size': pagination.size,
		'total_pages': pagination.total_pages,
		'total_elements': total_elements,
	}

	if len(employees) > 0:
		return Response(response, status=status.HTTP_200_OK)
	else:
		return Response({'detail': f"There are no employees matching your search"}, status=status.HTTP_204_NO_CONTENT)




@extend_schema(request=EmployeeSerializer, responses=EmployeeSerializer)
@api_view(['POST'])
@permission_classes([IsAuthenticated, IsAdminUser])
def createEmployee(request):
	data = request.data
	filtered_data = {}

	for key, value in data.items():
		if value != '' and value != 0 and value != '0':
			filtered_data[key] = value
			
	name = filtered_data.get('name', None)
	if name is not None:
		try:
			name = str(name).upper()
			employee = Employee.objects.get(name=name)
			return Response({'detail': f"Employee with name '{name}' already exists."})
		except Employee.DoesNotExist:
			pass

	serializer = EmployeeSerializer(data=filtered_data)

	if serializer.is_valid():
		serializer.save()
		return Response(serializer.data, status=status.HTTP_201_CREATED)
	else:
		return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)




@extend_schema(request=EmployeeSerializer, responses=EmployeeSerializer)
@api_view(['PUT'])
@permission_classes([IsAuthenticated, IsAdminUser])
def updateEmployee(request,pk):
	data = request.data
	filtered_data = {}
	try:
		employee = Employee.objects.get(pk=pk)
	except ObjectDoesNotExist:
		return Response({'detail': f'employee id - {pk} doesn\'t exists'}, status=status.HTTP_400_BAD_REQUEST)

	for key, value in data.items():
		if value != '' and value != 0 and value != '0':
			filtered_data[key] = value

	serializer = EmployeeSerializer(employee, data=filtered_data)
	if serializer.is_valid():
		serializer.save()
		return Response(serializer.data, status=status.HTTP_200_OK)
	else:
		return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)




@extend_schema(request=EmployeeSerializer, responses=EmployeeSerializer)
@api_view(['DELETE'])
@permission_classes([IsAuthenticated, IsAdminUser])
def deleteEmployee(request, pk):
	try:
		employee = Employee.objects.get(pk=pk)
		employee.delete()
		return Response({'detail': f'Employee id - {pk} is deleted successfully'}, status=status.HTTP_200_OK)
	except ObjectDoesNotExist:
		return Response({'detail': f"Employee id - {pk} doesn't exists"}, status=status.HTTP_400_BAD_REQUEST)

