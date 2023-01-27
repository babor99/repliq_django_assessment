from django.contrib.auth import get_user_model
from django_currentuser.middleware import (get_current_authenticated_user)
from rest_framework import serializers

from authentication.models import *

User = get_user_model()





class RoleMinSerializer(serializers.ModelSerializer):
	class Meta:
		model = Role
		fields = ['id', 'name']




class UserMinSerializer(serializers.ModelSerializer):
	class Meta:
		model = User
		fields = ['id', 'email', 'full_name', 'username', 'image']




class EmployeeMinSerializer(serializers.ModelSerializer):
	class Meta:
		model = Employee
		fields = ['id', 'full_name']




class PasswordChangeSerializer(serializers.Serializer):
	password = serializers.CharField(max_length=64)
	confirm_password = serializers.CharField(max_length=64)




class PermissionListSerializer(serializers.ModelSerializer):
	created_by = UserMinSerializer()
	updated_by = UserMinSerializer()
	class Meta:
		model = Permission
		fields = '__all__'
		extra_kwargs = {
			'created_at':{
				'read_only': True,
			},
			'updated_at':{
				'read_only': True,
			},
			'created_by':{
				'read_only': True,
			},
			'updated_by':{
				'read_only': True,
			},
		}
		
	def get_created_by(self, obj):
		return obj.created_by.email if obj.created_by else obj.created_by
		
	def get_updated_by(self, obj):
		return obj.updated_by.email if obj.updated_by else obj.updated_by




class PermissionSerializer(serializers.ModelSerializer):
	class Meta:
		model = Permission
		fields = '__all__'
		extra_kwargs = {
			'created_at':{
				'read_only': True,
			},
			'updated_at':{
				'read_only': True,
			},
			'created_by':{
				'read_only': True,
			},
			'updated_by':{
				'read_only': True,
			},
		}
		
	def create(self, validated_data):
		modelObject = super().create(validated_data=validated_data)
		user = get_current_authenticated_user()
		if user is not None:
			modelObject.created_by = user
		modelObject.save()
		return modelObject
	
	def update(self, instance, validated_data):
		modelObject = super().update(instance=instance, validated_data=validated_data)
		user = get_current_authenticated_user()
		if user is not None:
			modelObject.updated_by = user
		modelObject.save()
		return modelObject




class RoleListSerializer(serializers.ModelSerializer):
	created_by = UserMinSerializer()
	updated_by = UserMinSerializer()
	class Meta:
		model = Role
		fields = '__all__'
		extra_kwargs = {
			'created_at':{
				'read_only': True,
			},
			'updated_at':{
				'read_only': True,
			},
			'created_by':{
				'read_only': True,
			},
			'updated_by':{
				'read_only': True,
			},
		}
		
	def get_created_by(self, obj):
		return obj.created_by.email if obj.created_by else obj.created_by
		
	def get_updated_by(self, obj):
		return obj.updated_by.email if obj.updated_by else obj.updated_by




class RoleSerializer(serializers.ModelSerializer):
	class Meta:
		model = Role
		fields = '__all__'
		extra_kwargs = {
			'created_at':{
				'read_only': True,
			},
			'updated_at':{
				'read_only': True,
			},
			'created_by':{
				'read_only': True,
			},
			'updated_by':{
				'read_only': True,
			},
		}
		
	def create(self, validated_data):
		modelObject = super().create(validated_data=validated_data)
		user = get_current_authenticated_user()
		if user is not None:
			modelObject.created_by = user
		modelObject.save()
		return modelObject
	
	def update(self, instance, validated_data):
		modelObject = super().update(instance=instance, validated_data=validated_data)
		user = get_current_authenticated_user()
		if user is not None:
			modelObject.updated_by = user
		modelObject.save()
		return modelObject




class UserListSerializer(serializers.ModelSerializer):
	created_by = UserMinSerializer()
	updated_by = UserMinSerializer()
	
	class Meta:
		model = User
		exclude = ['user_type', 'is_active', 'is_admin', 'role', 'password']
		extra_kwargs = {
			'created_at':{
				'read_only': True,
			},
			'updated_at':{
				'read_only': True,
			},
			'created_by':{
				'read_only': True,
			},
			'updated_by':{
				'read_only': True,
			},
		}




class UserSerializer(serializers.ModelSerializer):
	class Meta:
		model = User
		exclude = ['user_type', 'is_active', 'is_admin', 'role']
		extra_kwargs = {
			'password': {
				'write_only': True,
				'required': False,
			},
			'created_at':{
				'read_only': True,
			},
			'updated_at':{
				'read_only': True,
			},
			'created_by':{
				'read_only': True,
			},
			'updated_by':{
				'read_only': True,
			},
		}

	def create(self, validated_data):
		modelObject = super().create(validated_data=validated_data)
		modelObject.set_password(validated_data["password"])
		user = get_current_authenticated_user()
		if user is not None:
			modelObject.created_by = user
		modelObject.save()
		return modelObject
	
	def update(self, instance, validated_data):
		modelObject = super().update(instance=instance, validated_data=validated_data)
		user = get_current_authenticated_user()
		if user is not None:
			modelObject.updated_by = user
		modelObject.save()
		return modelObject




class EmployeeListSerializer(serializers.ModelSerializer):
	created_by = UserMinSerializer()
	updated_by = UserMinSerializer()
	class Meta:
		model = Employee
		fields = '__all__'
		extra_kwargs = {
			'created_at':{
				'read_only': True,
			},
			'updated_at':{
				'read_only': True,
			},
			'created_by':{
				'read_only': True,
			},
			'updated_by':{
				'read_only': True,
			},
		}
		
	def get_created_by(self, obj):
		return obj.created_by.email if obj.created_by else obj.created_by
		
	def get_updated_by(self, obj):
		return obj.updated_by.email if obj.updated_by else obj.updated_by




class EmployeeSerializer(serializers.ModelSerializer):
	class Meta:
		model = Employee
		fields = '__all__'
		extra_kwargs = {
			'created_at':{
				'read_only': True,
			},
			'updated_at':{
				'read_only': True,
			},
			'created_by':{
				'read_only': True,
			},
			'updated_by':{
				'read_only': True,
			},
		}
		
	def create(self, validated_data):
		modelObject = super().create(validated_data=validated_data)
		user = get_current_authenticated_user()
		if user is not None:
			modelObject.created_by = user
		modelObject.save()
		return modelObject
	
	def update(self, instance, validated_data):
		modelObject = super().update(instance=instance, validated_data=validated_data)
		user = get_current_authenticated_user()
		if user is not None:
			modelObject.updated_by = user
		modelObject.save()
		return modelObject





