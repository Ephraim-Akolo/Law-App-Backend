
from django.urls import path, include
from . import views

urlpatterns = [
    path('gpt/', views.PureChatGPTView.as_view()),
]
