from rest_framework.serializers import ModelSerializer
from .models import application,plan,subscription
from users.models import User
class subscription_serializer(ModelSerializer):
    class Meta:
        model=subscription
        fields=['id','active','plan']

class application_serializer(ModelSerializer):
    app_subscription=subscription_serializer(read_only=True)

    class Meta:
        model=application
        fields='__all__'


class plan_serializer(ModelSerializer):
    class Meta:
        model=plan
        fields='__all__'

