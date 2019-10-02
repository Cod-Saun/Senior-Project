from django.urls import path
from . import views

urlpatterns = [ 
        path('', views.home, name="home"),
        path('TeachTool/', views.index, name="index"),
        path('Login/', views.login, name="login"),
        path('Register/', views.register, name="register"),
        path('Dashboard/', views.dashboard, name="dashboard"),
]
