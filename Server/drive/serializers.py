from rest_framework import serializers
from .models import File, Folder

LENGTH_OF_CASE_ID = 4


class FoldersSerializer(serializers.ModelSerializer):
    id = serializers.IntegerField(read_only=True)
    user = serializers.SerializerMethodField()
    name = serializers.SerializerMethodField()

    class Meta(object):
        model = Folder
        fields = ('id', 'user', 'name')

    def get_user(self, obj) -> serializers.EmailField:
        return obj.user.email
    
    def get_name(self, obj) -> str:
        return f'Case {"0"*(LENGTH_OF_CASE_ID-len(str(obj.id)))+str(obj.id)}'

    def create(self, validated_data):
        model = Folder.objects.create(user=self.context['request'].user)
        return model
    

# class FileSerializer(serializers.ModelSerializer):
#     id = serializers.IntegerField()
#     name = serializers.SerializerMethodField()
#     user = serializers.SerializerMethodField()
#     folder = FoldersSerializer(read_only=True, partial=True)
#     thumbnail = serializers.ImageField()
#     file = serializers.FileField(upload_to='files/')
#     created = serializers.DateTimeField()

#     class Meta(object):
#         model = File
#         fields = ('id', 'name', 'user', 'folder', 'thumbnail', 'file', 'created')

#     def get_user(self, obj):
#         return obj.folder.user.email
    
#     def get_name(self, obj):
#         return f'Case {"0"*(len(str(obj.id))-LENGTH_OF_CASE_ID)+str(obj.id)}'

#     def create(self, validated_data):
#         model_id = validated_data.pop("model_id")
#         prompt = validated_data.pop("prompt")
#         if model_id not in (1, 2):
#             raise serializers.ValidationError("model_id can only be (1, 2)")
#         response = get_engine(model_id).query(prompt)
#         model = LamaPrompt.objects.create(user=self.context['request'].user, prompt=prompt, response=response)
#         return model
