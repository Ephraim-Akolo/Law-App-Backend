from django.urls import path, include
# from rest_framework.authtoken.views import obtain_auth_token
from . import views
from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView,
)



urlpatterns = [
    path('signup/', views.UserSignupView.as_view()),
    path('api/login/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('api/login/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    # path('login/', obtain_auth_token),
]
