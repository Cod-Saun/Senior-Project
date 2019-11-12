from django.shortcuts import render, redirect, render_to_response
from django.http import HttpResponse
from django.http import JsonResponse
from django.contrib.auth.decorators import login_required
from django.template import RequestContext
from django.contrib.auth import logout
from django.utils.safestring import mark_safe
from . import forms
from . import models
import json

# Create your views here.
def home(request):
    context = {
        "loginredirect":""
    }
    return render(request, "home.html", context=context)

def register(request):
    if request.method == "POST":
        form_instance = forms.RegistrationForm(request.POST)
        if form_instance.is_valid():
            form_instance.save()
            return redirect("/Login")
    else:
        form_instance = forms.RegistrationForm()
    context = {
        "form":form_instance,
    }
    return render(request, "registration/register.html", context=context)

@login_required(login_url="/Login/")
def dashboard(request):
    return render(request, "dashboard.html")

@login_required(login_url="/Login/")
def create_quiz(request):
    quizform = forms.QuizCreation(request.POST or None)
    questionform = forms.QuestionCreation(request.POST or None)
    answerform = forms.AnswerCreation(request.POST or None)
    if quizform.is_valid() and questionform.is_valid() and answerform.is_valid():
        #quizform.cleaned_data()
        #questionform.cleaned_data()
        #answerform.cleaned_data()
        quiz = quizform.save()
        question = questionform.save()
        #question.quiz_id = quiz.quiz_id
        #question.save() 
        answer = answerform.save()
    
    context = {
        'quizform':quizform,
        'questionform':questionform,
        'answerform':answerform,
    }
    return render(request, "createquiz.html", context)

def Logout(request):
    logout(request)
    return redirect("/")
