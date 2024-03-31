import magic
from rest_framework import serializers
from django.db.models import Q
from .models import File, Folder, Thumbnail
from pathlib import Path
from . import utils

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
    file_content = serializers.SerializerMethodField()
    created = serializers.DateTimeField(read_only=True)

    class Meta(object):
        model = File
        fields = ('id', 'name', 'user', 'folder', 'add2folder', 'thumbnail', 'file', 'file_content', 'created')

    def get_user(self, obj) -> serializers.EmailField:
        if obj.folder:
            return obj.folder.user.email
        
    def get_thumbnail(self, obj)->serializers.ImageField:
        if obj.thumbnail:
            return obj.thumbnail.image.url
        
    def get_file_content(self, obj):
        url = obj.file.url
        # Use magic number detection to identify file type
        file_content = obj.file.read()
        mime_type = magic.from_buffer(file_content, mime=True)
        
        # Handle different file types
        if mime_type == 'application/pdf':
            return utils.read_pdf_from_url(url)
        elif mime_type == 'application/vnd.openxmlformats-officedocument.wordprocessingml.document':
            return utils.read_docx_from_url(url)
        elif mime_type.startswith('image/'):
            return utils.read_text_from_image_url(url)
        else:
            return utils.read_text_from_url(url)
    
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
    

class UpdateFileSerializer(serializers.ModelSerializer):
    name = serializers.SerializerMethodField()
    user = serializers.SerializerMethodField()
    file_name = serializers.CharField(write_only=True)
    new_folder = serializers.CharField(write_only=True)
    folder = FoldersSerializer(read_only=True)
    thumbnail = serializers.SerializerMethodField()
    file = serializers.FileField(read_only=True)
    file_content = serializers.SerializerMethodField()
    created = serializers.DateTimeField(read_only=True)

    class Meta(object):
        model = File
        fields = ('id', 'name', 'user', 'folder', 'new_folder', 'thumbnail', 'file', 'file_content', 'file_name', 'created')

    def get_user(self, obj) -> serializers.EmailField:
        if obj.folder:
            return obj.folder.user.email
        
    def get_thumbnail(self, obj)->serializers.ImageField:
        if obj.thumbnail:
            return obj.thumbnail.image.url
        
    def get_file_content(self, obj):
        url = obj.file.url
        # Use magic number detection to identify file type
        file_content = obj.file.read()
        mime_type = magic.from_buffer(file_content, mime=True)
        
        # Handle different file types
        if mime_type == 'application/pdf':
            return utils.read_pdf_from_url(url)
        elif mime_type == 'application/vnd.openxmlformats-officedocument.wordprocessingml.document':
            return utils.read_docx_from_url(url)
        elif mime_type.startswith('image/'):
            return utils.read_text_from_image_url(url)
        else:
            return utils.read_text_from_url(url)
    

    def get_name(self, obj) -> str:
        return f'Case {"0"*(LENGTH_OF_CASE_ID-len(str(obj.id)))+str(obj.id)}'
    

    def update(self, instance:File, validated_data):
        new_folder = validated_data.pop("new_folder")
        try:
            folder_id = int(new_folder.split(' ')[-1])
        except:
            raise serializers.ValidationError("Invalid folder name!")
        try:
            folder = Folder.objects.get(id=folder_id)
        except Folder.DoesNotExist:
            raise serializers.ValidationError("Folder does not exist!")
        instance.folder = folder
        instance.save()
        return instance
