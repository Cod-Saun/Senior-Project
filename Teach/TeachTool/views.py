from django.shortcuts import render, redirect, render_to_response
from django.http import HttpResponse, HttpResponseRedirect
from django.http import JsonResponse
from django.contrib.auth.decorators import login_required
from django.template import RequestContext
from django.contrib.auth import logout
from django.utils.safestring import mark_safe
from django.forms import modelformset_factory
from . import forms
from . import models
from .models import Quiz, QuizQuestion, QuizAnswer
import json

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

#Dislplay the form to create a quiz.
#Includes title, number of questions, and grade level
#Display form to create the questions of the quiz and its answers
#question will get quiz_id as a foreign key from the post request of the quiz creation form
#use formset to get multiple answer forms to show up
#find a way to get quiz_id as a foreign key while still submitting questions and answers at the same time
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
            return HttpResponseRedirect('QuestionCreation')
    else:
        context = {
            'quizform': quizform,
        }
        return render(request, "createquiz.html", context)

@login_required(login_url="/Login/")
def create_question(request):
    #get primary key of quiz that was created
    numquestions = request.session.get('numquestions')
    print(numquestions)

    questionformset = modelformset_factory(QuizQuestion, fields=('question_text',), extra=numquestions)
    questionform = questionformset(request.POST or None, queryset=QuizQuestion.objects.none())

#do this for each question form
    answerformset = modelformset_factory(QuizAnswer, fields=('answer_text', 'is_correct'), extra=4)
    answerform = answerformset(request.POST or None, queryset=QuizAnswer.objects.none())

    if questionform.is_valid(): #and answerform.is_valid():
        #retreive quizid from session and query for the quiz with the matching quizid
        quizid = request.session.get('quizid')
        quiz = Quiz(quiz_id=quizid)

        questions = questionform.save(commit=False)
        for question in questions:
            question.quiz_id = quiz
            print(question.quiz_id)
            question.save()

        #answers = answerform.save(commit=False)
        #for answer in answers:
            #answer.question_id = question
            #answer.save()
    context = {
        'questionform': questionform,
        #'answerform': answerform,
    }
    return render(request, "createquestion.html", context)

def Logout(request):
    logout(request)
    return redirect("/")