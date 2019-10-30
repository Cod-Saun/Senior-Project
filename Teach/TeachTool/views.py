from django.shortcuts import render, redirect, render_to_response
from django.http import HttpResponse
from django.http import JsonResponse
from django.contrib.auth.decorators import login_required
from django.template import RequestContext
from django.contrib.auth import logout
from django.utils.safestring import mark_safe
from . import forms
from .forms import QuizCreation
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
    if request.method =="POST":
        form = QuizCreation(request.POST)

        if form.is_valid():
            form.cleaned_data()
            print("success")
    else:
        form = QuizCreation()
    return render(request, "createquiz.html", {'form':form})

def Logout(request):
    logout(request)
    return redirect("/")