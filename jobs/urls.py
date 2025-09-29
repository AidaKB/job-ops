from django.urls import path
from . import views

urlpatterns = [
    path('', views.JobListCreateAPIView.as_view(), name='jobs'),
    path('<int:pk>/', views.JobDetailAPIView.as_view(), name='jobs_detail'),

    path('job-tasks/', views.JobTaskListCreateAPIView.as_view(), name='job_tasks'),
    path('job-tasks/<int:pk>/', views.JobTaskDetailAPIView.as_view(), name='job_tasks_detail'),
]
