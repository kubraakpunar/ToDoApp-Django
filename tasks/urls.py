from django.urls import path 
from . import views 

urlpatterns = [
    path('', views.index, name='index'),  # index view fonksiyonu için URL deseni
    path('update_task/<str:pk>/', views.updateTask, name='update_task'),
    path('delete/<str:pk>/', views.deleteTask, name='delete'),
    path('login/', views.login_view, name='login'), 
    path('register/', views.login_view, name='register'), 
]        