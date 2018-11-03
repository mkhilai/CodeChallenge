from rest_framework import serializers
from CodeChallenge.api.models import Users, Companies

class UsersSerializer(serializers.ModelSerializer):

	class Meta:
		model = Users
		fields = ('email', 'password', 'name')

class CompaniesSerializer(serializers.ModelSerializer):

	class Meta:
		model = Companies
		fields = ('name', 'email', 'phone', 'country', 'city', 'streetAddress')