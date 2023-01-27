from django.db import models
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager

from commons.mixins import CreatedUpdatedModelMixin



class Permission(CreatedUpdatedModelMixin):
	name = models.CharField(max_length=255)

	class Meta:
		ordering = ('-id',)
		verbose_name_plural = 'Permission'

	def __str__(self):
		return self.name
	
	def save(self, *args, **kwargs):
		self.name = self.name.replace(' ', '_').upper()
		super().save(*args, **kwargs)




class Role(CreatedUpdatedModelMixin):
	name = models.CharField(max_length=255)
	permissions = models.ManyToManyField(Permission, blank=True)

	class Meta:
		ordering = ('-id', )
		verbose_name_plural = 'Role'

	def __str__(self):
		return self.name
	
	def save(self, *args, **kwargs):
		self.name = self.name.replace(' ', '_').upper()
		super().save(*args, **kwargs)




class UserManager(BaseUserManager):
	def create_user(self, full_name, email, password=None, **kwargs):
		if not email:
			raise ValueError('User must have an email address')
			
		user = self.model(
			full_name=full_name,
			email=self.normalize_email(email),
			**kwargs
		)
		user.set_password(password)
		user.save(using=self._db)
		return user

	def create_superuser(self, full_name, email, password=None, **kwargs):
		user = self.create_user(
			full_name=full_name,
			email=email,
			password=password,
			**kwargs
		)
		user.is_admin = True
		user.save(using=self._db)
		return user
 


# this User model will be treated as Company
class User(AbstractBaseUser, CreatedUpdatedModelMixin):
	full_name = models.CharField(max_length=100)
	email = models.EmailField(verbose_name='email address', max_length=255, unique=True)
	username = models.CharField(max_length=255, unique=True)
	user_type = models.CharField(max_length=50, null=True, blank=True)
	phone = models.CharField(max_length=25, null=True, blank=True, unique=True)
	date_of_birth = models.DateField(null=True, blank=True)

	role = models.ForeignKey(Role, on_delete=models.SET_NULL, null=True, blank=True)

	is_active = models.BooleanField(default=True)
	is_admin = models.BooleanField(default=False)

	image = models.ImageField(upload_to="user/", null=True, blank=True)
	last_login = models.DateTimeField(auto_now_add=True)

	objects = UserManager()
	USERNAME_FIELD = 'email'
	REQUIRED_FIELDS = ['full_name']

	class Meta:
		ordering = ('-id', )
		verbose_name_plural = 'User/Company'

	def __str__(self):
		return self.full_name

	def has_perm(self, perm, obj=None):
		"Does the user have a specific permission?"
		# Simplest possible answer: Yes, always
		return True

	def has_module_perms(self, app_label):
		"Does the user have permissions to view the app `app_label`?"
		# Simplest possible answer: Yes, always
		return True

	@property
	def is_staff(self):
		"Is the user a member of staff?"
		# Simplest possible answer: All admins are staff
		return self.is_admin




class Employee(CreatedUpdatedModelMixin):
	company = models.ForeignKey(User, on_delete=models.CASCADE, related_name='company_employees')
	full_name = models.CharField(max_length=100)
	email = models.EmailField(verbose_name='email address', max_length=255, unique=True)
	phone = models.CharField(max_length=25, null=True, blank=True, unique=True)
	date_of_birth = models.DateField(null=True, blank=True)
	is_active = models.BooleanField(default=True)
	image = models.ImageField(upload_to="employee/", null=True, blank=True)

	class Meta:
		ordering = ('-id', )
		verbose_name_plural = 'Employee'

	def __str__(self):
		return self.full_name



