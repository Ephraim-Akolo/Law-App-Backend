from rest_framework import generics, permissions, mixins, exceptions
from rest_framework.parsers import MultiPartParser
from django.db.models import Q
from drf_spectacular.utils import extend_schema, extend_schema_view, OpenApiParameter
from . import serializers
from .models import File, Folder, Thumbnail

# Create your views here.


class FolderView(generics.ListCreateAPIView):
    serializer_class = serializers.FoldersSerializer
    permission_classes = (permissions.IsAuthenticated,)
    
    def get_queryset(self):
        return Folder.objects.filter(user=self.request.user).order_by('id')
    

    def get(self, request, *args, **kwargs):
        '''
        Get all folders.
        '''
        return super().get(request, *args, **kwargs)

    def post(self, request, *args, **kwargs):
        '''
        Create a folder for an authenticated user.
        '''
        return super().post(request, *args, **kwargs)
    

class FolderViewRD(generics.RetrieveDestroyAPIView):
    serializer_class = serializers.FoldersSerializer
    permission_classes = (permissions.IsAuthenticated,)

    def get_queryset(self):
        return Folder.objects.filter(user=self.request.user).order_by('id')
    
    def get_object(self):
        name = self.kwargs.get('name')
        id = int(name.split(' ')[-1])
        return self.get_queryset().filter(id=id).first()
    
    def get(self, request, *args, **kwargs):
        '''
        Get folder by name.
        '''
        return super().get(request, *args, **kwargs)
    
    def delete(self, request, *args, **kwargs):
        '''
        Delete a folder.
        '''
        return self.destroy(request, *args, **kwargs)
    

class ThumbnailView(generics.ListCreateAPIView):
    serializer_class = serializers.ThumbnailSerializer
    permission_classes = (permissions.IsAdminUser,)
    
    def get_queryset(self):
        return Thumbnail.objects.order_by('id')
    

    def get(self, request, *args, **kwargs):
        '''
        Get all Thumbnails.
        '''
        return super().get(request, *args, **kwargs)

    def post(self, request, *args, **kwargs):
        '''
        Create a thumbnail by an admin user.
        '''
        return super().post(request, *args, **kwargs)
    
    
@extend_schema_view(
    get=extend_schema(
        parameters=[
            OpenApiParameter(name='folder', description='Folder Name', type=str),
        ]
    )
)
class FileView(generics.ListCreateAPIView):
    serializer_class = serializers.FileSerializer
    permission_classes = (permissions.IsAuthenticatedOrReadOnly,)
    parser_classes = (MultiPartParser,)
    
    def get_queryset(self):
        folder = self.request.GET.get('folder', None)
        if folder is not None and self.request.user.is_authenticated is False:
            raise exceptions.ValidationError("Login to access your private folders!")
        
        if folder == 'all':
            return File.objects.filter(Q(folder=None)|Q(folder__user=self.request.user)).order_by('id')
        
        elif folder:
            try:
                folder_id = int(folder.split(' ')[-1])
            except Exception as e:
                raise exceptions.ValidationError("Incorrect folder name!")
            
            return File.objects.filter(folder__id=folder_id, folder__user=self.request.user).order_by('id')
        
        return File.objects.filter(folder=None).order_by('id')
    

    def get(self, request, *args, **kwargs):
        '''
        Get all folders.
        '''
        return super().get(request, *args, **kwargs)
    

    def post(self, request, *args, **kwargs):
        '''
        Create a folder for an authenticated user.
        '''
        return super().post(request, *args, **kwargs)


# class FileView(generics.ListCreateAPIView):
#     # serializer_class = serializers.GetLamaResponseSerializer
#     permission_classes = (permissions.IsAuthenticated,)
    
#     def get_queryset(self):
#         return File.objects.filter(folder__user=self.request.user).order_by('id')

#     def post(self, request, *args, **kwargs):
#         '''
#         Get all files accessible to the user.
#         '''
#         return super().post(request, *args, **kwargs)

