from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('start/', views.trigger_agent, name='start_agent'),
    path('status/<str:task_id>/', views.get_task_status, name='task_status'), # <--- New Line
]