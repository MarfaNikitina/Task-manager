from django.urls import path
from . import views

urlpatterns = [
    path('', views.UserListView.as_view(), name='users'),
    path('create/', views.UserCreateView.as_view()),
    path('<int:pk>/update/', views.UserUpdateView.as_view(), name="update"),
    path('<int:pk>/delete/', views.UserDeleteView.as_view(), name='delete'),
]