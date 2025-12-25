from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name='index'),
    
    # 🔴 CHANGE: 'trigger_agent' -> 'start_task'
    path('start/', views.start_task, name='start_agent'), 
    
    path('status/<str:task_id>/', views.get_status, name='get_status'),
]