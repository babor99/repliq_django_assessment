from django.core.exceptions import ObjectDoesNotExist

from rest_framework import status
from rest_framework.decorators import api_view, permission_classes
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated

from drf_spectacular.utils import  extend_schema, OpenApiParameter

from authentication.decorators import IsAdminUser, has_permissions

from device.models import Category
from device.serializers import CategorySerializer, CategoryListSerializer

from commons.pagination import Pagination




# Create your views here.

@extend_schema(
	parameters=[
		OpenApiParameter("page"),
		OpenApiParameter("size"),
  ],
	request=CategorySerializer,
	responses=CategorySerializer
)
@api_view(['GET'])
@permission_classes([IsAuthenticated, IsAdminUser])
# @has_permissions([PermissionEnum.PERMISSION_LIST_VIEW.name])
def getAllCategory(request):
	categories = Category.objects.all()
	total_elements = categories.count()

	page = request.query_params.get('page')
	size = request.query_params.get('size')

	# Pagination
	pagination = Pagination()
	pagination.page = page
	pagination.size = size
	categories = pagination.paginate_data(categories)

	serializer = CategoryListSerializer(categories, many=True)

	response = {
		'categories': serializer.data,
		'page': pagination.page,
		'size': pagination.size,
		'total_pages': pagination.total_pages,
		'total_elements': total_elements,
	}

	return Response(response, status=status.HTTP_200_OK)




@extend_schema(
	request=CategorySerializer,
	responses=CategorySerializer
)
@api_view(['GET'])
@permission_classes([IsAuthenticated, IsAdminUser])
# @has_permissions([PermissionEnum.PERMISSION_LIST_VIEW.name])
def getAllCategoryWithoutPagination(request):
	categories = Category.objects.all()

	serializer = CategoryListSerializer(categories, many=True)

	return Response({'categories': serializer.data}, status=status.HTTP_200_OK)




@extend_schema(request=CategorySerializer, responses=CategorySerializer)
@api_view(['GET'])
@permission_classes([IsAuthenticated, IsAdminUser])
def getACategory(request, pk):
	try:
		category = Category.objects.get(pk=pk)
		serializer = CategorySerializer(category)
		return Response(serializer.data, status=status.HTTP_200_OK)
	except ObjectDoesNotExist:
		return Response({'detail': f"Category id - {pk} doesn't exists"}, status=status.HTTP_400_BAD_REQUEST)




@extend_schema(
	parameters=[
		OpenApiParameter('key'),
		OpenApiParameter('page'),
		OpenApiParameter('size'),
		],
	request=CategorySerializer, 
	responses=CategorySerializer)
@api_view(['GET'])
@permission_classes([IsAuthenticated, IsAdminUser])
# @has_permissions([PermissionEnum.PRODUCT_DETAILS.name])
def searchCategory(request):
	key = request.query_params.get('key')
	categories = Category.objects.filter(name__icontains=key)

	total_elements = categories.count()

	page = request.query_params.get('page')
	size = request.query_params.get('size')

	# Pagination
	pagination = Pagination()
	pagination.page = page
	pagination.size = size
	categories = pagination.paginate_data(categories)

	serializer = CategoryListSerializer(categories, many=True)

	response = {
		'categories': serializer.data,
		'page': pagination.page,
		'size': pagination.size,
		'total_pages': pagination.total_pages,
		'total_elements': total_elements,
	}

	if len(categories) > 0:
		return Response(response, status=status.HTTP_200_OK)
	else:
		return Response({'detail': f"There are no categories matching your search"}, status=status.HTTP_204_NO_CONTENT)




@extend_schema(request=CategorySerializer, responses=CategorySerializer)
@api_view(['POST'])
@permission_classes([IsAuthenticated, IsAdminUser])
def createCategory(request):
	data = request.data
	filtered_data = {}

	for key, value in data.items():
		if value != '' and value != 0 and value != '0':
			filtered_data[key] = value
			
	name = filtered_data.get('name', None)
	if name is not None:
		try:
			name = str(name).upper()
			category = Category.objects.get(name=name)
			return Response({'detail': f"Category with name '{name}' already exists."})
		except Category.DoesNotExist:
			pass

	serializer = CategorySerializer(data=filtered_data)

	if serializer.is_valid():
		serializer.save()
		return Response(serializer.data, status=status.HTTP_201_CREATED)
	else:
		return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)




@extend_schema(request=CategorySerializer, responses=CategorySerializer)
@api_view(['PUT'])
@permission_classes([IsAuthenticated, IsAdminUser])
def updateCategory(request,pk):
	data = request.data
	filtered_data = {}
	try:
		category = Category.objects.get(pk=pk)
	except ObjectDoesNotExist:
		return Response({'detail': f'category id - {pk} doesn\'t exists'}, status=status.HTTP_400_BAD_REQUEST)

	for key, value in data.items():
		if value != '' and value != 0 and value != '0':
			filtered_data[key] = value

	serializer = CategorySerializer(category, data=filtered_data)
	if serializer.is_valid():
		serializer.save()
		return Response(serializer.data, status=status.HTTP_200_OK)
	else:
		return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)




@extend_schema(request=CategorySerializer, responses=CategorySerializer)
@api_view(['DELETE'])
@permission_classes([IsAuthenticated, IsAdminUser])
def deleteCategory(request, pk):
	try:
		category = Category.objects.get(pk=pk)
		category.delete()
		return Response({'detail': f'Category id - {pk} is deleted successfully'}, status=status.HTTP_200_OK)
	except ObjectDoesNotExist:
		return Response({'detail': f"Category id - {pk} doesn't exists"}, status=status.HTTP_400_BAD_REQUEST)

