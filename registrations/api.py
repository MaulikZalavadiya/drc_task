from rest_framework.permissions import AllowAny
from rest_framework.viewsets import ModelViewSet

from custom_auth.models import User
from .serializers import RegistrationSerializer



class RegistrationViewSet(ModelViewSet):
    queryset = User.objects.all()
    serializer_class = RegistrationSerializer
    permission_classes = [AllowAny]
