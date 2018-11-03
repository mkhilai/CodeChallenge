from rest_framework import status, generics
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from django.db import transaction
from CodeChallenge.api.serializers import UsersSerializer
from CodeChallenge.api.models import Users, Companies

class CreateUsers(generics.CreateAPIView):
	serializer_class = UsersSerializer

	def create(self, request, *args, **kwargs):
		serializer = self.get_serializer(data=request.data)
		serializer.is_valid(raise_exception=True)
		with transaction.atomic():
			user = serializer.save()
		return Response(serializer.data, status=status.HTTP_201_CREATED)