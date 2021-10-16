import json
import coreapi, coreschema
from django.contrib.auth.hashers import check_password
from drf_yasg import openapi
from drf_yasg.utils import swagger_auto_schema
from rest_framework import renderers

from .models import User
from django.shortcuts import render
from django.contrib.auth import get_user_model
from django.contrib.auth.mixins import LoginRequiredMixin
from django.urls import reverse
from django.views.generic import DetailView, RedirectView, UpdateView
from rest_framework.exceptions import ValidationError
from rest_framework.response import Response
from rest_framework.authentication import TokenAuthentication
from rest_framework.decorators import api_view, permission_classes, authentication_classes, renderer_classes, schema
from rest_framework.permissions import AllowAny, IsAuthenticated, IsAdminUser
from rest_framework.authtoken.models import Token




@swagger_auto_schema(method='post', request_body=openapi.Schema(
    type=openapi.TYPE_OBJECT,
    properties={
        'email': openapi.Schema(type=openapi.TYPE_STRING, description='email of user'),
        'password':openapi.Schema(type=openapi.TYPE_STRING, description='password of user'),
        'password_again':openapi.Schema(type=openapi.TYPE_STRING, description='password again'),

    },required=['email','password','password_again']),
    responses={200: 'application created successfully',400: 'Bad Request'})
@api_view(['POST'])
@authentication_classes([TokenAuthentication])
@permission_classes([AllowAny])
def Registeration(request):


    email=request.data['email']
    password=request.data['password']
    password_again=request.data['password_again']
    if password!=password_again:
        response_object = {}
        meta = {"code": 400, "message": "failure"}

        response_object['meta'] = meta
        response_object['data'] = 'passwords donot match'

    used=User.objects.get_or_create(email=email)
    if used[1]==False:
        response_object = {}
        meta = {"code": 400, "message": "failure"}

        response_object['meta'] = meta
        response_object['data'] = 'User already exists'


    else:
        used[0].set_password(password)
        used[0].username=email
        toke=Token.objects.create(user=used[0]).key
        used[0].save()

    response_object = {}
    meta = {"code": 1000, "message": "success"}
    data = {}
    data['message'] = 'User Registered Successfully'
    data['email_address'] = used[0].email
    data['Token'] = toke
    response_object['meta'] = meta
    response_object['data'] = data
    return Response(response_object)

@swagger_auto_schema(method='post', request_body=openapi.Schema(
    type=openapi.TYPE_OBJECT,
    properties={
        'email': openapi.Schema(type=openapi.TYPE_STRING, description='email of user'),
        'password':openapi.Schema(type=openapi.TYPE_STRING, description='password of user'),


    },required=['email','password']),
    responses={200: 'application created successfully',400: 'Bad Request'})
@api_view(["POST"])
@authentication_classes([TokenAuthentication])
@permission_classes([AllowAny])
def login_user(request):
    data = {}
    reqBody = request.data
    email1 = reqBody['email']

    password = reqBody['password']
    try:

        Account = User.objects.get(email=email1)

    except BaseException as e:
        raise ValidationError({"Error": f'{str(e)}'})

    token = Token.objects.get_or_create(user=Account)[0].key

    if not check_password(password, Account.password):
        raise ValidationError({"message": "Incorrect Login credentials"})

    if Account:
        if Account.is_active:

            data["message"] = "user logged in"
            data["email_address"] = Account.email
            data['id'] = Account.id
            data['token']=token
            response_object = {}
            meta = {"code": 1000, "message": "success"}
            response_object['meta'] = meta
            response_object['data'] = data

            return Response(response_object)

        else:
            raise ValidationError({"Error": f'Account not active'})

    else:
        raise ValidationError({"Error": f'Account doesnt exist'})





class UserDetailView(LoginRequiredMixin, DetailView):

    model = User
    slug_field = "username"
    slug_url_kwarg = "username"


user_detail_view = UserDetailView.as_view()


class UserUpdateView(LoginRequiredMixin, UpdateView):

    model = User
    fields = ["name"]

    def get_success_url(self):
        return reverse("users:detail", kwargs={"username": self.request.user.username})

    def get_object(self):
        return User.objects.get(username=self.request.user.username)


user_update_view = UserUpdateView.as_view()


class UserRedirectView(LoginRequiredMixin, RedirectView):

    permanent = False

    def get_redirect_url(self):
        return reverse("users:detail", kwargs={"username": self.request.user.username})


user_redirect_view = UserRedirectView.as_view()
