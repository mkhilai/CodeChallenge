from django.contrib import admin
from django.conf.urls import url
from CodeChallenge.api.views import CreateUsers, ListCreateCompanies

urlpatterns = [
	url(r'admin/', admin.site.urls),
	url(r'users/', CreateUsers.as_view(), name='users'),
	url(r'companies/', ListCreateCompanies.as_view(), name='companies')
]
