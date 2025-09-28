from django.urls import path
from . import views

urlpatterns = [
    path('', views.JobListCreateAPIView.as_view(), name='jobs'),
    path('<int:pk>/', views.JobDetailAPIView.as_view(), name='jobs_detail'),
]
