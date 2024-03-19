
from django.urls import path, include
from . import views

urlpatterns = [
    path('folder/', views.FolderView.as_view()),
    path('folder/<str:name>/', views.FolderViewRD.as_view()),
    path('file/', views.FileView.as_view()),
    path('thumbnail/', views.ThumbnailView.as_view()),
    # path('file/<str:name>/', views.FolderViewRD.as_view()),
]

#create a folder
#get all folders
# get all folders for user
#create a file
#Create a file in folder
# change a file to folder
#get all files
#get all files in folder
#get all files by user
#delete file
#delete folder