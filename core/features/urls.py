from django.urls import path
from . import views

app_name = 'features'

urlpatterns = [
    path('', views.welcome, name='welcome'),
    path('main/', views.main, name='main'),
]
