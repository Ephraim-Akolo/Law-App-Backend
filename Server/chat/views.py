from rest_framework import generics, permissions
from . import serializers
from .models import ChatGPTPrompt, LamaPrompt

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


class LamaView(generics.ListCreateAPIView):
    serializer_class = serializers.GetLamaResponseSerializer
    permission_classes = (permissions.IsAuthenticated,)
    
    def get_queryset(self):
        return LamaPrompt.objects.filter(user=self.request.user).order_by('id')

    def post(self, request, *args, **kwargs):
        '''
        Make a request to our custom lama index model running on top of chatgpt model, trained with the `Nigerian criminal code document`.
        '''
        return super().post(request, *args, **kwargs)

