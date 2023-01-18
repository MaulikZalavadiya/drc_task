from django.urls import path, include
from rest_framework import routers
from .api import *
router = routers.SimpleRouter()


app_name = 'custom-auth'

urlpatterns = [
    path('', include(router.urls)),
    path('send_otp/', Send_opt_API),
    path('login', LoginAPI),
    path('logout', LogoutAPI),
]
