import json
import yaml
from django.shortcuts import render
from django.db.models import Q
from drf_yasg import openapi
from drf_yasg.utils import swagger_auto_schema
from rest_framework.exceptions import ValidationError
from rest_framework.response import Response
from rest_framework.authentication import TokenAuthentication, SessionAuthentication
from rest_framework.decorators import api_view, permission_classes, authentication_classes, schema
from rest_framework.permissions import AllowAny, IsAuthenticated, IsAdminUser
from rest_framework.schemas.openapi import AutoSchema
from rest_framework.views import APIView
from .models import application,plan,subscription
from .serializer import application_serializer,plan_serializer

# Create your views here.


@swagger_auto_schema(method='post', request_body=openapi.Schema(
    type=openapi.TYPE_OBJECT,
    properties={
        'name': openapi.Schema(type=openapi.TYPE_STRING, description='name of application'),
        'description':openapi.Schema(type=openapi.TYPE_STRING, description='description'),

    },required=['name','description']),
    responses={200: 'application created successfully',400: 'Bad Request'})
@api_view(["POST"])
@authentication_classes([TokenAuthentication,SessionAuthentication])
@permission_classes([IsAuthenticated])
def create_application(request):
    try:

        reqBody = request.data
        name=reqBody['name']
        description=reqBody['description']
        application_to_create=application.objects.create(user=request.user,
                                                                name=name,description=description)
        response_object = {}
        meta = {"code": 1000, "message": "application created successfully"}
        data = {}
        data['application_id']=application_to_create.id
        response_object['meta'] = meta
        response_object['data'] = data
        return Response(response_object)

    except BaseException as e:
        raise ValidationError({"error":str(e)})




@swagger_auto_schema(method='get',
                manual_parameters=[openapi.Parameter('id', openapi.IN_QUERY, description="id of application", type=openapi.TYPE_INTEGER)],
                responses={200: application_serializer,400: 'Bad Request'})
@api_view(["GET"])
@authentication_classes([TokenAuthentication,SessionAuthentication])
@permission_classes([IsAuthenticated])
def retrieve_applications(request):
    try:
        id_number=request.GET.get('id')

        application_to_get=application.objects.get(id=id_number)
        serialized=application_serializer(instance=application_to_get)

        response_object = {}
        meta = {"code": 1000, "message": "success"}
        data = {}
        response_object['meta'] = meta
        response_object['data'] = serialized.data
        return Response(response_object)

    except BaseException as e:
        raise ValidationError({"error":str(e)})


@swagger_auto_schema(method='get',
                responses={200: application_serializer,400: 'Bad Request'})
@api_view(["GET"])
@authentication_classes([TokenAuthentication,SessionAuthentication])
@permission_classes([IsAuthenticated])
def get_all_applications(request):
    try:


        application_to_get=application.objects.filter(user=request.user)
        serialized=application_serializer(instance=application_to_get,many=True)

        response_object = {}
        meta = {"code": 1000, "message": "successfully retrieved all application"}
        data = {}
        response_object['meta'] = meta
        response_object['data'] = serialized.data
        return Response(response_object)

    except BaseException as e:
        raise ValidationError({"error":str(e)})





@swagger_auto_schema(method='put',
                manual_parameters=[openapi.Parameter('id', openapi.IN_QUERY, description="id of application", type=openapi.TYPE_INTEGER)],
                request_body=openapi.Schema(
                         type=openapi.TYPE_OBJECT,
                         properties={
                             'name': openapi.Schema(type=openapi.TYPE_STRING, description='name of application'),
                             'description': openapi.Schema(type=openapi.TYPE_STRING, description='description'),

                         }),
                        required=['name','description'],
                responses={200: application_serializer,400: 'Bad Request'})
@api_view(["PUT"])
@authentication_classes([TokenAuthentication,SessionAuthentication])
@permission_classes([IsAuthenticated])
def update_application(request):
    try:
        id_number=request.GET.get('id')
        print(request.data)
        if 'name' in request.data.keys():
            application_to_get = application.objects.get(id=id_number)
            application_to_get.name=request.data['name']
            application_to_get.save()

        if 'description' in request.data.keys():
            application_to_get = application.objects.get(id=id_number)
            application_to_get.description = request.data['description']
            application_to_get.save()

        else:
            return Response('You didnot provide any value to change')

        application_to_get=application.objects.get(id=id_number)
        serialized=application_serializer(instance=application_to_get)

        response_object = {}
        meta = {"code": 1000, "message": "application updated successfully"}
        data = {}
        response_object['meta'] = meta
        response_object['data'] = serialized.data
        return Response(response_object)

    except BaseException as e:
        raise ValidationError({"error":str(e)})

@swagger_auto_schema(method='delete',
                manual_parameters=[openapi.Parameter('name', openapi.IN_QUERY, description="name of application", type=openapi.TYPE_STRING)],
                responses={200: application_serializer,400: 'Bad Request'})
@api_view(["DELETE"])
@authentication_classes([TokenAuthentication,SessionAuthentication])
@permission_classes([IsAuthenticated])
def delete_application(request):
    try:
        name_application=request.GET.get('name')
        print(name_application)


        application_to_get = application.objects.get(user=request.user,name=name_application)
        application_to_get.delete()


        response_object = {}
        meta = {"code": 1000, "message": "application deleted successfully"}
        data = {}
        response_object['meta'] = meta
        response_object['data'] = data
        return Response(response_object)

    except BaseException as e:
        raise ValidationError({"error":str(e)})


@swagger_auto_schema(method='get',
                responses={200: application_serializer,400: 'Bad Request'})
@api_view(["GET"])
@authentication_classes([TokenAuthentication,SessionAuthentication])
@permission_classes([IsAuthenticated])
def get_all_plans(request):
    all_plans=plan.objects.all()
    serialized=plan_serializer(instance=all_plans,many=True)
    response_object = {}
    meta = {"code": 1000, "message": "all plans listed"}
    data = {}
    response_object['meta'] = meta
    response_object['data'] = serialized.data
    return Response(response_object)


@swagger_auto_schema(method='get',
                manual_parameters=[openapi.Parameter('id', openapi.IN_QUERY, description="id of plan", type=openapi.TYPE_INTEGER)],
                responses={200: application_serializer,400: 'Bad Request'})
@api_view(["GET"])
@authentication_classes([TokenAuthentication,SessionAuthentication])
@permission_classes([IsAuthenticated])
def get_specific_plan(request):
    id_of_plan=request.GET.get('id')
    plan_to_retrieve=plan.objects.get(id=id_of_plan)
    serialized = plan_serializer(instance=plan_to_retrieve)
    response_object = {}
    meta = {"code": 1000, "message": "plan listed"}
    data = {}
    response_object['meta'] = meta
    response_object['data'] = serialized.data
    return Response(response_object)

