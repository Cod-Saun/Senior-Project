from . import forms
from . import models
from .models import Quiz, QuizQuestion, QuizAnswer
from django.shortcuts import render, redirect, render_to_response
from django.http import HttpResponse, HttpResponseRedirect
from django.contrib.auth.decorators import login_required
from django.template import RequestContext
from django.contrib.auth import logout
from django.utils.safestring import mark_safe
from django.forms import inlineformset_factory

# Create your views here.
def home(request):
    context = {
        "loginredirect": ""
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
        "form": form_instance,
    }
    return render(request, "registration/register.html", context=context)

@login_required(login_url="/Login/")
def dashboard(request):
    return render(request, "dashboard.html")

@login_required(login_url="/Login/")
def create_quiz(request):
    quizform = forms.QuizCreation(request.POST or None)

    if request.method == 'POST':
        if quizform.is_valid():
            quiz = quizform.save()
            quizid = quiz.quiz_id
            numquestions = quiz.num_questions
            request.session['quizid'] = quizid
            request.session['numquestions'] = numquestions
            return redirect('./QuestionCreation')
    else:
        context = {
            'quizform': quizform,
        }
        return render(request, "createquiz.html", context)

@login_required(login_url="/Login/")
def create_question(request):
    #get primary key of quiz that was created
    numquestions = request.session.get('numquestions')
    quizid = request.session.get('quizid')
    quiz = Quiz(quiz_id=quizid)

    questionform = forms.QuestionCreation(request.POST or None)
    AnswerFormSet = inlineformset_factory(QuizQuestion, QuizAnswer, fields=('answer_text', 'is_correct',), extra=4, can_delete=False)
    formset = AnswerFormSet(request.POST or None)
    
    if request.method == 'POST' and numquestions > 1 :
        if questionform.is_valid():
            question = questionform.save(commit=False)
            question.quiz_id = quiz
            question.save()

        formset.instance = question
        if formset.is_valid():
            formset.save()
            numquestions = numquestions - 1
            request.session['numquestions'] = numquestions
            return redirect('./QuestionCreation')
    elif request.method == 'POST' and numquestions == 1:
        if questionform.is_valid():
            question = questionform.save(commit=False)
            question.quiz_id = quiz
            question.save()

        formset.instance = question
        if formset.is_valid():
            formset.save()
            return redirect('/Dashboard')
    else:
        context = {
            'questionform':questionform,
            'formset':formset,
            'numquestions':numquestions
        }
        return render(request, "createquestion.html", context)

def Logout(request):
    logout(request)
    return redirect("/")