from rest_framework import generics, permissions
from . import serializers
from .models import ChatGPTPrompt

# Create your views here.


class PureChatGPTView(generics.ListCreateAPIView):
    serializer_class = serializers.GetChatGPTResponseSerializer
    permission_classes = (permissions.IsAuthenticated,)
    
    def get_queryset(self):
        return ChatGPTPrompt.objects.filter(user=self.request.user).order_by('id')

    def post(self, request, *args, **kwargs):
        '''
        Make a request directly to ChatGPT.
        '''
        return super().post(request, *args, **kwargs)
