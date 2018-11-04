from django.db import models
from django.contrib.auth.models import AbstractUser
from django.db.models.signals import post_save
from django.dispatch import receiver
from CodeChallenge import settings
from rest_framework.authtoken.models import Token
from django.contrib.auth.models import  BaseUserManager

@receiver(post_save, sender=settings.AUTH_USER_MODEL)
def create_auth_token(sender, instance=None, created=False, **kwargs):
	if created:
		Token.objects.create(user=instance)

class Users(AbstractUser):
	userID = models.AutoField(db_column='userID', primary_key=True)
	username = models.CharField(max_length=64, unique=True)
	email = models.EmailField(db_column='email', max_length=64, db_index=True, unique=True)
	password = models.CharField(db_column='password', max_length=16)
	name = models.CharField(db_column='name', max_length=64, null=True)

	USERNAME_FIELD = 'username'
	REQUIRED_FIELDS = ('email',)

	def __str__(self):
		return self.email

	class Meta:
		ordering = ['userID']
		db_table = 'Users'

class Companies(models.Model):
	companyID = models.AutoField(db_column='companyID', primary_key=True)
	name = models.CharField(db_column='name', max_length=200)
	email = models.EmailField(db_column='email', max_length=64, db_index=True, unique=True)
	phone = models.CharField(db_column='phone', max_length=16, unique=True)
	country = models.CharField(db_column='country', max_length=64, null=True)
	city = models.CharField(db_column='city', max_length=64, null=True)
	streetAddress = models.CharField(db_column='street', max_length=124, null=True)
	userID = models.ForeignKey(db_column='userID', to='Users', on_delete=models.PROTECT, null=True)

	def __str__(self):
		return self.name

	class Meta:
		ordering = ['companyID']
		db_table = 'Companies'


