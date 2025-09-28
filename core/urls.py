from django.urls import path
from . import views
from dj_rest_auth.views import LogoutView
from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView,
    TokenBlacklistView,
)

urlpatterns = [
    path('auth/login/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('auth/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    path('auth/logout/', TokenBlacklistView.as_view(), name='token_blacklist'),

    path('users/', views.CustomUserListCreateAPIView.as_view(), name='user_signup'),
    path('users/<int:pk>/', views.CustomUserDetailAPIView.as_view(), name='user_detail'),
]
