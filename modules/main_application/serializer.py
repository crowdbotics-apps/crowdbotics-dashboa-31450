from rest_framework.serializers import ModelSerializer
from .models import application,plan,subscription
from users.models import User


class application_serializer(ModelSerializer):
    class Meta:
        model=application
        fields='__all__'


class plan_serializer(ModelSerializer):
    class Meta:
        model=plan
        fields='__all__'