from django.conf import settings
from django.conf.urls.static import static
from django.conf.urls import url
from django.urls import path
from django.contrib.auth import views as auth_views
from . import views

urlpatterns = [ 
        path('', views.home),
        path('Login/', auth_views.LoginView.as_view()),
        path('Register/', views.register),
        path('Dashboard/', views.dashboard),
        path('Logout/', views.Logout),
]
