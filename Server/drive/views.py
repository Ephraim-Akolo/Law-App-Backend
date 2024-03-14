from rest_framework import generics, permissions, mixins
from . import serializers
from .models import File, Folder

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

