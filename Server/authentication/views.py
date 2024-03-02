from rest_framework import generics
from . import serializers
# Create your views here.


class UserSignupView(generics.CreateAPIView):
    serializer_class = serializers.CreateUserSerializer
   
    