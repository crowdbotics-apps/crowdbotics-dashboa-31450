from django.db import models
from users.models import User

# Create your models here.

class application(models.Model):
    user=models.ForeignKey(User,on_delete=models.CASCADE,null=True,blank=True,related_name='application')
    name=models.CharField(max_length=264,null=True,blank=True,unique=True)
    description=models.TextField(max_length=100,null=True,blank=True)
    type=models.CharField(max_length=100,null=True,blank=True)
    framework=models.CharField(max_length=100,null=True,blank=True)
    updated_at=models.DateTimeField(auto_now=True)



plan_choices=(('Free','Free'),('Standard','Standard'),('Pro','Pro'))
class plan(models.Model):
    type_of_plan=models.CharField(max_length=264,null=True,blank=True,choices=plan_choices)
    price=models.IntegerField(null=True,blank=True)
    created_at=models.DateTimeField(auto_now=True)



class subscription(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, null=True, blank=True, related_name='user_subscription')
    plan=models.ForeignKey(plan, on_delete=models.CASCADE, null=True, blank=True, related_name='plan_subscription')
    application = models.OneToOneField(application, on_delete=models.CASCADE, null=True, blank=True,
                                    related_name='app_subscription')
    active=models.BooleanField(default=False)


