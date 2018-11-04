from rest_framework import serializers
from CodeChallenge.api.models import Users, Companies

class UsersSerializer(serializers.ModelSerializer):

	class Meta:
		model = Users
		fields = ('userID', 'username', 'email', 'password', 'name')

	def create(self, validated_data):
		user = super(UsersSerializer, self).create(validated_data)
		user.set_password(validated_data['password'])
		user.save()
		return user

class CompaniesSerializer(serializers.ModelSerializer):

	class Meta:
		model = Companies
		fields = ('companyID', 'name', 'email', 'phone', 'country', 'city', 'streetAddress')