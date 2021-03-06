from django.contrib import admin
from django.conf.urls import url
from CodeChallenge.api.views import CreateUsers, ListCreateCompanies, CompanyDetails, LogInView
from rest_framework.authtoken import views

urlpatterns = [
	url(r'^users/$', CreateUsers.as_view(), name='users'),
	url(r'^companies/$', ListCreateCompanies.as_view(), name='companies'),
	url(r'^companies/(?P<pk>[0-9]+)/$', CompanyDetails.as_view(), name='companies'),
	url(r'^login/$', LogInView.as_view(), name='login'),
]
