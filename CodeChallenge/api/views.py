from rest_framework import status, generics
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from rest_framework.views import APIView
from django.db import transaction
from CodeChallenge.api.serializers import UsersSerializer, CompaniesSerializer
from CodeChallenge.api.models import Users, Companies
from django.contrib.auth import authenticate
from rest_framework.authtoken.models import Token


class CreateUsers(generics.CreateAPIView):
	serializer_class = UsersSerializer

	def create(self, request, *args, **kwargs):
		serializer = self.get_serializer(data=request.data)
		serializer.is_valid(raise_exception=True)
		with transaction.atomic():
			user = serializer.save()
			return Response(serializer.data, status=status.HTTP_201_CREATED)
		return Response(status=status.HTTP_400_BAD_REQUEST)

class ListCreateCompanies(generics.ListCreateAPIView):
	queryset = Companies.objects.all()
	serializer_class = CompaniesSerializer
	permission_classes = (IsAuthenticated,)

	def list(self, request):
		queryset = Companies.objects.filter(userID=request.user.userID)
		serializer = CompaniesSerializer(queryset, many=True)
		return Response(serializer.data, status=status.HTTP_200_OK)

	def create(self, request, *args, **kwargs):
		serializer = self.get_serializer(data=request.data, many=True)
		serializer.is_valid(raise_exception=True)
		with transaction.atomic():
			user_instance = Users.objects.get(userID=request.user.userID)
			companies = serializer.save()
			for company in companies:
				company.userID = user_instance
				company.save()
			return Response(serializer.data, status=status.HTTP_201_CREATED)
		return Response(status=status.HTTP_400_BAD_REQUEST)

class CompanyDetails(generics.RetrieveUpdateDestroyAPIView):
	queryset = Companies.objects.all()
	serializer_class = CompaniesSerializer
	permission_classes = (IsAuthenticated,)

	def update_instance(self, request, is_partial):
		instance = self.get_object()
		serializer = self.get_serializer(instance, data=request.data, partial=is_partial)
		serializer.is_valid(raise_exception=True)
		serializer.save()
		return serializer

	def get(self, request, *args, **kwargs):
		instance = self.get_object()
		serializer = self.get_serializer(instance)
		return Response(serializer.data, status=status.HTTP_200_OK)

	def update(self, request, *args, **kwargs):
		response = self.update_instance(request, is_partial=False)
		return Response(response.data, status=status.HTTP_200_OK)

	def partial_update(self, request, *args, **kwargs):
		response = self.update_instance(request, is_partial=True)
		return Response(response.data, status=status.HTTP_200_OK)

	def delete(self, request, *args, **kwargs):
		instance = self.get_object()
		print(instance)
		if request.user.userID == instance.userID.userID:
			instance.delete()
			return Response(status=status.HTTP_200_OK)
		return Response(status=status.HTTP_401_UNAUTHORIZED)

class LogInView(APIView):

	def post(self, request):
		username = request.data.get("username")
		password = request.data.get("password")
		if username and password:
			user = authenticate(username=username, password=password)
			if user:
				token, _ = Token.objects.get_or_create(user=user)
				return Response({'token': token.key}, status=status.HTTP_200_OK)
			else:
				return Response('Invalid Credentials', status=status.HTTP_404_NOT_FOUND)


