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
    path('QuizCreation/', views.create_quiz),
    path('QuizCreation/QuestionCreation', views.create_question),
    path('Quiz/<quizid>/', views.quizintro),
    path('Quiz/<quizid>/<questionid>/', views.quiz),
    path('Student/<studentid>/', views.student),
    path('StudentCreation/', views.create_student)
]