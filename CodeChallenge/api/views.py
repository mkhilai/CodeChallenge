from rest_framework import status, generics
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from django.db import transaction
from CodeChallenge.api.serializers import UsersSerializer, CompaniesSerializer
from CodeChallenge.api.models import Users, Companies

class CreateUsers(generics.CreateAPIView):
	serializer_class = UsersSerializer

	def create(self, request, *args, **kwargs):
		serializer = self.get_serializer(data=request.data)
		serializer.is_valid(raise_exception=True)
		with transaction.atomic():
			user = serializer.save()
		return Response(serializer.data, status=status.HTTP_201_CREATED)

class ListCreateCompanies(generics.ListCreateAPIView):
	queryset = Companies.objects.all()
	serializer_class = CompaniesSerializer
	permission_classes = (IsAuthenticated,)

	def list(self, request):
		queryset = Companies.objects.filter(userID=self.request.user.userID)
		serializer = CompaniesSerializer(queryset, many=True)
		return Response(serializer.data, status=status.HTTP_200_OK)

	def create(self, request, *args, **kwargs):
		serializer = self.get_serializer(data=request.data, many=True)
		serializer.is_valid(raise_exception=True)
		with transaction.atomic():
			user_instance = Users.objects.get(userID=self.request.user.userID)
			companies = serializer.save()
			for company in companies:
				company.userID = user_instance
				company.save()
		return Response(serializer.data, status=status.HTTP_201_CREATED)