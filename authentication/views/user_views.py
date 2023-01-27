from django.contrib.auth import get_user_model
from django.contrib.auth.hashers import make_password
from django.core.exceptions import ObjectDoesNotExist
from django.utils import timezone
from django.db.models import Q
from django.core.exceptions import PermissionDenied

from rest_framework import status
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer
from rest_framework_simplejwt.views import TokenObtainPairView

from drf_spectacular.utils import OpenApiParameter, extend_schema

from authentication.decorators import has_permissions, IsAdminUser
from authentication.models import Permission
from authentication.serializers import (UserSerializer, PasswordChangeSerializer, UserListSerializer)

from commons.enums import PermissionEnum
from commons.pagination import Pagination



# Create your views here.
User = get_user_model()


class MyTokenObtainPairSerializer(TokenObtainPairSerializer):
	def validate(self, attrs):
		data = super().validate(attrs)
		user_data = UserListSerializer(self.user).data
		data['user'] = user_data
		return data


class MyTokenObtainPairView(TokenObtainPairView):
    serializer_class = MyTokenObtainPairSerializer




@extend_schema(
	parameters=[
		OpenApiParameter("page"),
		OpenApiParameter("size"),
  ],
	request=UserSerializer,
	responses=UserSerializer
)
@api_view(['GET'])
@permission_classes([IsAuthenticated, IsAdminUser])
# @has_permissions([PermissionEnum.PERMISSION_LIST.name])
def getAllUser(request):
	users = User.objects.all()
	total_elements = users.count()

	page = request.query_params.get('page')
	size = request.query_params.get('size')

	# Pagination
	pagination = Pagination()
	pagination.page = page
	pagination.size = size
	users = pagination.paginate_data(users)

	serializer = UserListSerializer(users, many=True)

	response = {
		'users': serializer.data,
		'page': pagination.page,
		'size': pagination.size,
		'total_pages': pagination.total_pages,
		'total_elements': total_elements,
	}

	return Response(response, status=status.HTTP_200_OK)




@extend_schema(
	request=UserSerializer,
	responses=UserSerializer
)
@api_view(['GET'])
@permission_classes([IsAuthenticated, IsAdminUser])
# @has_permissions([PermissionEnum.PERMISSION_LIST.name])
def getAllUserWithoutPagination(request):
	users = User.objects.all()

	serializer = UserListSerializer(users, many=True)

	return Response({'users': serializer.data}, status=status.HTTP_200_OK)




@extend_schema(request=UserSerializer, responses=UserSerializer)
@api_view(['GET'])
@permission_classes([IsAuthenticated, IsAdminUser])
# @has_permissions([PermissionEnum.USER_DETAILS.name])
def getAUser(request, pk):
	try:
		user = User.objects.get(pk=pk)
		serializer = UserSerializer(user)
		return Response(serializer.data)
	except ObjectDoesNotExist:
		return Response({'detail': f"User id - {pk} doesn't exists"})




@extend_schema(request=UserSerializer, responses=UserSerializer)
@api_view(['GET'])
@permission_classes([IsAuthenticated])
# @has_permissions([PermissionEnum.USER_DETAILS.name])
def getMySelfUser(request):
	try:
		user = request.user
		print('user: ', user)
		serializer = UserListSerializer(user)
		return Response(serializer.data, status=status.HTTP_200_OK)
	except ObjectDoesNotExist:
		return Response({'detail': f"User doesn't exists"}, status=status.HTTP_400_BAD_REQUEST)




@extend_schema(request=UserSerializer, responses=UserSerializer)
@api_view(['GET'])
@permission_classes([IsAuthenticated])
# @has_permissions([PermissionEnum.USER_DETAILS.name])
def verifyMySelfUser(request):
	try:
		user = request.user
		if user:
			return Response({'is_authenticated': True}, status=status.HTTP_200_OK)
		else:
			return Response(status=status.HTTP_400_BAD_REQUEST)
	except ObjectDoesNotExist:
		return Response(status=status.HTTP_400_BAD_REQUEST)




@extend_schema(request=UserSerializer, responses=UserSerializer)
@api_view(['POST'])
# @permission_classes([IsAuthenticated])
# @has_permissions([PermissionEnum.USER_CREATE.name])
def createUser(request):
	data = request.data
	user_data_dict = {}
	current_datetime = timezone.now()
	current_datetime = str(current_datetime)
	restricted_values = ('', ' ', 0, 'undefined')

	print('data: ', request.data)

	for key, value in data.items():
		if value not in restricted_values:
			user_data_dict[key] = value
		
	user_data_dict['last_login'] = current_datetime

	serializer = UserSerializer(data=user_data_dict, many=False)

	if serializer.is_valid():
		serializer.save()
		return Response(serializer.data, status=status.HTTP_201_CREATED)
	else:
		return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)




@extend_schema(request=UserSerializer, responses=UserSerializer)
@api_view(['PUT'])
@permission_classes([IsAuthenticated, IsAdminUser])
# @has_permissions([PermissionEnum.USER_UPDATE.name])
def updateUser(request, pk):
	data = request.data
	filtered_data = {}
	restricted_values = (0, '', 'undefined', ' ')

	for key, value in data.items():
		if value not in restricted_values:
			filtered_data[key] = value

	image = data.get('image')
	if image and type(image) == str:
		filtered_data.pop('image')

	try:
		user = User.objects.get(pk=pk)
		serializer = UserSerializer(user, data=filtered_data, partial=True)
		if serializer.is_valid():
			serializer.save()
			return Response(serializer.data, status=status.HTTP_200_OK)
		else:
			return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
	except ObjectDoesNotExist:
		return Response({'detail': f"User id - {pk} doesn't exists"})




@extend_schema(request=UserSerializer, responses=UserSerializer)
@api_view(['PUT'])
@permission_classes([IsAuthenticated])
# @has_permissions([PermissionEnum.USER_UPDATE.name])
def updateMySelfUser(request):
	data = request.data
	print('data: ', data)
	try:
		user = request.user
		serializer = UserSerializer(user, data=data, partial=True)
		if serializer.is_valid():
			serializer.save()
			return Response(serializer.data, status=status.HTTP_200_OK)
		else:
			return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
	except ObjectDoesNotExist:
		return Response({'detail': f"User doesn't exist"})





@extend_schema(
	parameters=[
		OpenApiParameter("permission"),
  ],
	request=UserSerializer,
	responses=UserSerializer
)
@api_view(['GET'])
@permission_classes([IsAuthenticated])
# @has_permissions([PermissionEnum.USER_UPDATE.name])
def userHasPermission(request):
	permission_param = request.query_params.get('permission')
	user = request.user

	try:
		permission = Permission.objects.get(name=permission_param)
	except:
		response = {'detail': f"There is no such permission named '{permission_param}'."}
		return Response(response, status=status.HTTP_400_BAD_REQUEST)


	get_permission = user.role.permissions.get(pk=permission.id)

	if get_permission:
		return Response({'permission': True}, status=status.HTTP_200_OK)
	else:
		response = {'detail': f"Pemission denied! this user has no '{permission_param}' permission."}
		return Response(response, status=status.HTTP_400_BAD_REQUEST)




@extend_schema(request=PasswordChangeSerializer)
@api_view(['PATCH'])
@permission_classes([IsAuthenticated])
def userPasswordChange(request, pk):
	current_password = request.data['current_password']
	new_password1 = request.data['new_password1']
	new_password2 = request.data['new_password2']
	try:
		user = User.objects.get(pk=pk)

		if new_password1 == new_password2:
			if user.check_password(current_password):
				user.password = make_password(new_password1)
				user.save()
				return Response({'detail': f"User password has been changed successfully"}, status=status.HTTP_200_OK)
			else:
				return Response({'detail': f"Authentication failed. Wrong password"}, status=status.HTTP_401_UNAUTHORIZED)
		else:
			return Response({'detail': f"Password didn't match"}, status=status.HTTP_400_BAD_REQUEST)
	except ObjectDoesNotExist:
		return Response({'detail': f"User doesn't exist"}, status=status.HTTP_400_BAD_REQUEST)




@api_view(['POST'])
@permission_classes([IsAuthenticated])
def userImageUpload(request, pk):
	try:
		user = User.objects.get(pk=pk)
		data = request.data
		# image = 

		if 'image' in data:
			user.image = data['image']
			user.save()
			return Response(user.image.url, status=status.HTTP_200_OK)
		else:
			response = {'detail': f"Please upload a valid image"}
			return Response(response, status=status.HTTP_400_BAD_REQUEST)
	except ObjectDoesNotExist:
		response = {'detail': f"User id - {pk} doesn't exists"}
		return Response(response, status=status.HTTP_400_BAD_REQUEST)




@extend_schema(request=UserSerializer, responses=UserSerializer)
@api_view(['DELETE'])
@permission_classes([IsAuthenticated])
# @has_permissions([PermissionEnum.USER_DELETE.name])
def deleteMySelfUser(request):
	password = request.data.get('password', '')
	print(request.data)
	print('request.user: ', request.user)
	try:
		user = request.user
		if user.check_password(password):
			user.delete()
			return Response({'detail': f'User is deleted successfully'}, status=status.HTTP_200_OK)
		else:
			return Response({'detail': f'Authentication failed!'}, status=status.HTTP_400_BAD_REQUEST)
	except ObjectDoesNotExist:
		return Response({'detail': f"User doesn't exists"}, status=status.HTTP_400_BAD_REQUEST)




@extend_schema(request=UserSerializer, responses=UserSerializer)
@api_view(['DELETE'])
@permission_classes([IsAuthenticated, IsAdminUser])
# @has_permissions([PermissionEnum.USER_DELETE.name])
def deleteUser(request, pk):
	try:
		user = User.objects.get(pk=pk)
		user.delete()
		return Response({'detail': f'User id - {pk} is deleted successfully'}, status=status.HTTP_200_OK)
	except ObjectDoesNotExist:
		return Response({'detail': f"User id - {pk} doesn't exists"}, status=status.HTTP_400_BAD_REQUEST)



	
	