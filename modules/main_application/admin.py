from django.contrib import admin
from .models import application,subscription,plan
# Register your models here.
admin.site.register(application)
admin.site.register(subscription)
admin.site.register(plan)