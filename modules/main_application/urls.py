from django.contrib import admin
from django.urls import path, include
from modules.main_application import views

# application/




urlpatterns = [
    path('create_application/',views.create_application),
    path('retrieve_application/',views.retrieve_applications),
    path('update_application/',views.update_application),
    path('delete_application/',views.delete_application),
    path('get_all_applications/',views. get_all_applications),
    path('get_all_plans/',views.get_all_plans),
    path('get_specific_plan/',views.get_specific_plan)

]
