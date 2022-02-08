from rest_framework.viewsets import ModelViewSet
from api.models import User
from api.serializers import UserSerializer
from rest_framework.viewsets import ModelViewSet

from api.models import User
from api.serializers import UserSerializer


# Create your views here.

class UserViewSet(ModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer
