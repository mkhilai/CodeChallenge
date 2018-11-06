from rest_framework.test import APITestCase
from rest_framework import status
from CodeChallenge.api.models import Users, Companies
from rest_framework.authtoken.models import Token

class UsersTest(APITestCase):

	def get_user_data(self):
		return {
			"username": "test_user",
			"email": "test_user@test.com",
			"password": "testpassword",
			"name": "testname"
		}

	def check_if_can_create_a_user(self, expected_status, expected_number_of_objects, field_to_remove=None):
		data = self.get_user_data()

		if field_to_remove and field_to_remove in data:
			data.pop(field_to_remove)

		response = self.client.post('/users/', data, format='json')

		self.assertEqual(response.status_code, expected_status)

		if 'email' in data:
			get_queryset = Users.objects.filter(email=data['email'])

			if expected_status == status.HTTP_201_CREATED or status.HTTP_200_OK:
				self.assertEqual(get_queryset.count(), expected_number_of_objects)

			if get_queryset.count() > 0:
				for item in get_queryset:
					self.assertEqual(item.username, data['username'])
					self.assertEqual(item.email, data['email'])

	def test_can_create_a_user_with_full_data(self):
		self.check_if_can_create_a_user(status.HTTP_201_CREATED, 1)

	def test_can_create_a_user_without_name(self):
		self.check_if_can_create_a_user(status.HTTP_201_CREATED, 1, 'name')

	def test_cannot_create_a_user_without_username(self):
		self.check_if_can_create_a_user(status.HTTP_400_BAD_REQUEST, 0, 'username')

	def test_cannot_create_a_user_without_password(self):
		self.check_if_can_create_a_user(status.HTTP_400_BAD_REQUEST, 0, 'password')

	def test_cannot_create_a_user_without_email(self):
		self.check_if_can_create_a_user(status.HTTP_400_BAD_REQUEST, 0, 'email')

class CompaniesTest(APITestCase):

	def setUp(self):
		self.TestUserA = Users.objects.create_user('Test User A', 'test_user_a@test.com', 'testpassword')
		self.TestUserB = Users.objects.create_user('Test User B', 'test_user_b@test.com', 'testpassword')

	def get_companies_data(self):
		return [
			{
				"name": "Test Company",
				"email": "test_company@test.com",
				"phone": "+49 123 4567890",
				"country": "Country",
				"city": "City",
				"streetAddress": "City 123 00 B",
				"userID": self.TestUserA.userID
			},
			{
				"name": "Another Company",
				"email": "anotehr_company@test.com",
				"phone": "+49 456 1237890",
				"country": "Country",
				"city": "City",
				"streetAddress": "City 321 99 C",
				"userID": self.TestUserA.userID
			}
		]

	def get_token(self, user):
		response = self.client.post('/login/', {"username":user.username, "password":"testpassword"}, format='json')
		token = 'Token ' + response.data['token']
		return token

	def check_if_can_create_a_company(self, expected_status, expected_number_of_objects, field_to_remove=None):
		data = self.get_companies_data()

		if field_to_remove:
			for item in data:
				item.pop(field_to_remove)

		response = self.client.post('/companies/', data, format='json', HTTP_AUTHORIZATION=self.get_token(self.TestUserA))

		self.assertEqual(response.status_code, expected_status)

		get_instances = Companies.objects.all()
		number_of_objects = get_instances.count()

		self.assertEqual(number_of_objects, expected_number_of_objects)

		if number_of_objects > 0:
			for index in range(number_of_objects):
				if 'name' in data:
					self.assertEqual(get_instances[index].name, data[index]['name'])
				if 'email' in data:
					self.assertEqual(get_instances[index].email, data[index]['email'])
				if 'phone' in data:
					self.assertEqual(get_instances[index].phone, data[index]['phone'])
				if 'country' in data:
					self.assertEqual(get_instances[index].country, data[index]['country'])
				if 'city' in data:
					self.assertEqual(get_instances[index].city, data[index]['city'])
				if 'streetAddress' in data:
					self.assertEqual(get_instances[index].streetAddress, data[index]['streetAddress'])

	def test_can_create_a_company_if_user_logged_in_and_with_full_company_data(self):
		self.check_if_can_create_a_company(status.HTTP_201_CREATED, 2)

	def test_can_create_a_company_if_user_logged_in_and_without_company_country(self):
		self.check_if_can_create_a_company(status.HTTP_201_CREATED, 2, 'country')

	def test_can_create_a_company_if_user_logged_in_and_without_company_city(self):
		self.check_if_can_create_a_company(status.HTTP_201_CREATED, 2, 'city')

	def test_can_create_a_company_if_user_logged_in_and_without_company_street_address(self):
		self.check_if_can_create_a_company(status.HTTP_201_CREATED, 2, 'streetAddress')

	def test_cannot_create_a_company_if_user_logged_in_and_without_company_name(self):
		self.check_if_can_create_a_company(status.HTTP_400_BAD_REQUEST, 0, 'name')

	def test_cannot_create_a_company_if_user_logged_in_and_without_company_email(self):
		self.check_if_can_create_a_company(status.HTTP_400_BAD_REQUEST, 0, 'email')

	def test_cannot_create_a_company_if_user_logged_in_and_without_company_phone(self):
		self.check_if_can_create_a_company(status.HTTP_400_BAD_REQUEST, 0, 'phone')

	def test_cannot_create_companies_if_user_is_not_logged_in(self):
		data = self.get_companies_data()
		response = self.client.post('/companies/', data, format='json')
		get_instances = Companies.objects.all()
		self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)
		self.assertEqual(get_instances.count(), 0)

	def test_can_get_companies(self):
		data = self.get_companies_data()
		response = self.client.post('/companies/', data, format='json', HTTP_AUTHORIZATION=self.get_token(self.TestUserA))
		get_instances = Companies.objects.all()
		self.assertEqual(response.status_code, status.HTTP_201_CREATED)
		self.assertEqual(get_instances.count(), 2)

	def test_cannot_get_companies_if_user_is_not_logged_in(self):
		data = self.get_companies_data()
		post_response = self.client.post('/companies/', data, format='json', HTTP_AUTHORIZATION=self.get_token(self.TestUserA))
		get_response = self.client.get('/companies/', format='json')
		get_instances = Companies.objects.all()
		self.assertEqual(post_response.status_code, status.HTTP_201_CREATED)
		self.assertEqual(get_instances.count(), 2)
		self.assertEqual(get_response.status_code, status.HTTP_401_UNAUTHORIZED)
		self.assertNotEqual(len(get_response.data), 2)
	
	def test_cannot_get_companies_if_different_user_is_logged_in(self):
		data = self.get_companies_data()
		post_response = self.client.post('/companies/', data, format='json', HTTP_AUTHORIZATION=self.get_token(self.TestUserA))
		get_response = self.client.get('/companies/', format='json', HTTP_AUTHORIZATION=self.get_token(self.TestUserB))
		get_instances = Companies.objects.all()
		self.assertEqual(post_response.status_code, status.HTTP_201_CREATED)
		self.assertEqual(get_instances.count(), 2)
		self.assertEqual(get_response.status_code, status.HTTP_200_OK)
		self.assertNotEqual(len(get_response.data), 2)


class GetTokenTest(APITestCase):
	def setUp(self):
		self.TestUserA = Users.objects.create_user('Test User A', 'test_user_a@test.com', 'testpassword')

	def test_get_token(self):
		data = {
			"username": "Test User A",
			"password": "testpassword"
		}
		post_response = self.client.post('/login/', data, format='json')
		token = Token.objects.get(user__email = self.TestUserA.email, user__password = self.TestUserA.password)

		self.assertEqual(post_response.status_code, status.HTTP_200_OK)
		self.assertEqual(post_response.data['token'], token.key)
		






