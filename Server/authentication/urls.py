from django.urls import path, include
# from rest_framework.authtoken.views import obtain_auth_token
from . import views

urlpatterns = [
    path('signup/', views.UserSignupView.as_view()),
    # path('login/', obtain_auth_token),
]
