from rest_framework import serializers
from django.db.models import Q
from .models import File, Folder, Thumbnail
from pathlib import Path

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
    

class ThumbnailSerializer(serializers.ModelSerializer):
    ext = serializers.CharField()
    image = serializers.ImageField()

    class Meta(object):
        model = Thumbnail
        fields = ("ext", "image")
    
    def create(self, validated_data):
        ext = validated_data.pop('ext')
        image = validated_data.pop('image')
        if ext[0] != '.':
            ext = f".{ext}"
        thumbnail = Thumbnail.objects.create(ext=ext, image=image)
        return thumbnail
    

class FileSerializer(serializers.ModelSerializer):
    id = serializers.IntegerField(read_only=True)
    name = serializers.SerializerMethodField()
    user = serializers.SerializerMethodField()
    add2folder = serializers.CharField(write_only=True, allow_blank=True)
    folder = FoldersSerializer(read_only=True)
    thumbnail = serializers.SerializerMethodField()
    file = serializers.FileField()
    created = serializers.DateTimeField(read_only=True)

    class Meta(object):
        model = File
        fields = ('id', 'name', 'user', 'folder', 'add2folder', 'thumbnail', 'file', 'created')

    def get_user(self, obj) -> serializers.EmailField:
        if obj.folder:
            return obj.folder.user.email
        
    def get_thumbnail(self, obj)->serializers.ImageField:
        if obj.thumbnail:
            return obj.thumbnail.image.url
    
    def get_name(self, obj) -> str:
        return f'Case {"0"*(LENGTH_OF_CASE_ID-len(str(obj.id)))+str(obj.id)}'

    def create(self, validated_data):
        add2folder = validated_data.pop("add2folder")
        file = validated_data.pop("file")
        try:
            folder = Folder.objects.get(id=int(add2folder.split(' ')[-1]), user=self.context['request'].user) if add2folder and add2folder.isalnum() else None
            ext = Path(file.name).suffix.lower()
            thumbnail = Thumbnail.objects.filter(ext__iexact=ext).first()
            if thumbnail is None:
                thumbnail = Thumbnail.objects.filter(ext='.all').first()
        except Folder.DoesNotExist:
            print("The folder name entered does not exist for user")
        instance = File.objects.create(folder=folder, file=file, thumbnail=thumbnail)
        return instance
