from django.urls import path
from . import views

urlpatterns = [
    path('', views.EquipmentListCreateAPIView.as_view(), name='equipments'),
    path('<int:pk>/', views.EquipmentDetailAPIView.as_view(), name='equipments_detail'),
]