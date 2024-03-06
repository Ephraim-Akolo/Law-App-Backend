from rest_framework import serializers
from .models import ChatGPTPrompt
from .chatgpt import get_completion


class GetChatGPTResponseSerializer(serializers.ModelSerializer):
    user = serializers.SerializerMethodField()
    prompt = serializers.CharField()
    response = serializers.CharField(read_only=True)

    class Meta(object):
        model = ChatGPTPrompt
        fields = ('user', 'prompt', 'response')

    def get_user(self, obj):
        return obj.user.email


    def create(self, validated_data):
        prompt = validated_data.pop("prompt")
        response = get_completion(prompt)
        model = ChatGPTPrompt.objects.create(user=self.context['request'].user, prompt=prompt, response=response)
        return model
