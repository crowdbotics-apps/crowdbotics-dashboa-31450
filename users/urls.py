from django.urls import path
from drf_yasg.views import get_schema_view
from rest_framework import permissions
from rest_framework.routers import DefaultRouter
from drf_yasg import openapi

from users.views import (
Registeration,login_user
)
# users/
app_name = "users"
urlpatterns = [

    path('register/',Registeration),
    path('login/',login_user)

]




