from rest_framework import serializers
from .models import ChatGPTPrompt, LamaPrompt
from .chatgpt import get_completion
from .llm import get_engine


class GetChatGPTResponseSerializer(serializers.ModelSerializer):
    user = serializers.SerializerMethodField()
    prompt = serializers.CharField()
    response = serializers.CharField(read_only=True)

    class Meta(object):
        model = ChatGPTPrompt
        fields = ('user', 'prompt', 'response')

    def get_user(self, obj)->serializers.EmailField:
        return obj.user.email


    def create(self, validated_data):
        prompt = validated_data.pop("prompt")
        response = get_completion(prompt)
        model = ChatGPTPrompt.objects.create(user=self.context['request'].user, prompt=prompt, response=response)
        return model
    

class GetLamaResponseSerializer(serializers.ModelSerializer):
    user = serializers.SerializerMethodField()
    prompt = serializers.CharField()
    model_id = serializers.IntegerField(default=1, write_only=True)
    response = serializers.CharField(read_only=True)

    class Meta(object):
        model = LamaPrompt
        fields = ('user', 'prompt', 'response', 'model_id')

    def get_user(self, obj) -> serializers.EmailField:
        return obj.user.email


    def create(self, validated_data):
        model_id = validated_data.pop("model_id")
        prompt = validated_data.pop("prompt")
        if model_id not in (1, 2):
            raise serializers.ValidationError("model_id can only be (1, 2)")
        response = get_engine(model_id).query(prompt)
        model = LamaPrompt.objects.create(user=self.context['request'].user, prompt=prompt, response=response)
        return model
