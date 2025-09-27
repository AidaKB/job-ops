from django.urls import path
from . import views
from dj_rest_auth.views import LogoutView
from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView,
)

urlpatterns = [
    # path('auth/signup/admin/', views.AdminSignUpAPIView.as_view(), name='admin_signup'),
    # path('auth/signup/institute/', views.InstituteSignUpAPIView.as_view(), name='institute_signup'),
    # path('auth/signup/teacher/', views.TeacherSignUpAPIView.as_view(), name='teacher_signup'),
    # path('auth/signup/student/', views.StudentSignUpAPIView.as_view(), name='student_signup'),

    path('auth/login/', views.CustomLoginView.as_view(), name='custom_login'),
    path('auth/logout/', LogoutView.as_view(), name='custom_logout'),

    path('token/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),

]
