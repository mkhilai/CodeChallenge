from django.contrib import admin
from django.conf.urls import url
from CodeChallenge.api.views import CreateUsers

urlpatterns = [
	url(r'admin/', admin.site.urls),
	url(r'users/', CreateUsers.as_view(), name='users'),
]
