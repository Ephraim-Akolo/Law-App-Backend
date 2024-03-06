from rest_framework import generics
from . import serializers
# Create your views here.


class UserSignupView(generics.CreateAPIView):
    serializer_class = serializers.CreateUserSerializer

    def post(self, request, *args, **kwargs):
        '''
        Create a user account on the platform if it does not exist.
        '''
        return super().post(request, *args, **kwargs)
   
    