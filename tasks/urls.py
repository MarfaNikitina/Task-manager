from django.urls import path
from . import views

urlpatterns = [
    path('', views.TasksListView.as_view(), name='statuses'),
    path('create/', views.TasksCreateView.as_view(), name='create_task'),
    path('<int:pk>/update/', views.TasksUpdateView.as_view(), name="update_task"),
    path('<int:pk>/delete/', views.TasksDeleteView.as_view(), name='delete_task'),
]