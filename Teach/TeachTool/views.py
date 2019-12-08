from . import forms
from . import models
from .models import *
from django.shortcuts import render, redirect, render_to_response
from django.http import HttpResponse, HttpResponseRedirect
from django.contrib.auth.decorators import login_required
from django.template import RequestContext
from django.contrib.auth import logout
from django.utils.safestring import mark_safe
from django.forms import inlineformset_factory, ModelChoiceField

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
    quizzes = Quiz.objects.all()
    students = Student.objects.all()
    context = {
        'students':students,
        'quizzes':quizzes,
    }
    return render(request, "dashboard.html", context)

@login_required(login_url="/Login/")
def quizintro(request, quizid):
    studentform = forms.SelectStudent(request.POST or None)
    quiz = Quiz.objects.get(quiz_id=quizid)
    questions = QuizQuestion.objects.filter(quiz_id=quiz)
    question = questions[0]
    if request.method == "POST":
        if studentform.is_valid():
            student = studentform.cleaned_data['students']
            studentid = student.student_id
            results = QuizResult.objects.filter(quiz_id=quiz, student_id=student).order_by('-attempt')
            if results.count() > 0 and results[0].attempt >= 1:
                result = QuizResult(quiz_id=quiz, student_id=student, score=0, attempt=results[0].attempt + 1)
                result.save()
            else:
                result = QuizResult(quiz_id=quiz, student_id=student, score=0, attempt=1)
                result.save()
            request.session['studentid'] = studentid
            return redirect('/Quiz/' + str(quiz.quiz_id) + '/' + str(question.question_id) +'/')
        
    context = { 
        'quiz':quiz,
        'question':question,
        'studentform':studentform,
    }
    return render(request, "quizintro.html", context)

def quiz(request, quizid, questionid):
    quiz = Quiz.objects.get(quiz_id=quizid)
    question = QuizQuestion.objects.get(question_id=questionid)
    questions = QuizQuestion.objects.filter(quiz_id=quiz)
    answers = QuizAnswer.objects.filter(question_id=questionid)
    correct_answer = answers.get(is_correct=True)
    answerform = forms.SelectAnswer(request.POST or None, answers=answers)
    studentid = request.session.get('studentid')
    student = Student.objects.get(student_id=studentid)
    nextquestion = str(int(questionid) + 1)
    lastquestion = False

    if request.method == 'POST':
        if answerform.is_valid():
            selectedanswer = answerform.cleaned_data['answer_text']
            selectedanswerid = answers.filter(answer_text=selectedanswer)
            studentanswer = StudentAnswer(question=question, student_id=student, correct_answer=correct_answer, student_answer=selectedanswerid[0])
            studentanswer.save()
            if str(studentanswer.student_answer) == correct_answer.answer_text:
                result = QuizResult.objects.filter(student_id=student, quiz_id=quiz).order_by('-attempt')
                result = result[0]
                result.score = result.score + 1
                result.save()
            else:
                result = QuizResult.objects.filter(student_id=student, quiz_id=quiz).order_by('-attempt')
                result = result[0]

        if int(questionid) == questions.last().question_id:
            return redirect('/Results/' + quizid + '/' + str(studentid) + '/' + str(result.result_id) + '/')
        else:
            lastquestion = False
            return redirect('/Quiz/' + quizid + '/' + nextquestion + '/')

    if int(questionid) == questions.last().question_id:
        lastquestion = True

    context = {
        'quizid':quizid,
        'question':question,
        'nextquestion':nextquestion,
        'lastquestion':lastquestion,
        'answers':answers,
        'answerform':answerform,
    }
    return render(request, "quiz.html", context)

def quizresults(request, studentid, quizid, resultid):
    result = QuizResult.objects.get(result_id=resultid)
    quiz = Quiz.objects.get(quiz_id=quizid)
    quizname = quiz.quiz_title
    student = Student.objects.get(student_id=studentid)
    studentname = student.first_name + ' ' + student.last_name
    score = (result.score / quiz.num_questions) * 100
    context = {
        'quizname':quizname,
        'studentname':studentname,
        'score':score,
    }
    return render(request, "quizresults.html", context)

def student(request, studentid):
    student = Student.objects.get(student_id=studentid)
    results = QuizResult.objects.filter(student_id=studentid)
    context = {
        'student':student,
        'results':results,
    }
    return render(request, "student.html", context)

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

@login_required(login_url="/Login/")
def create_student(request):
    studentform = forms.StudentCreation(request.POST or None)
    if request.method == 'POST':
        if studentform.is_valid():
            student = studentform.save()
            return redirect('/Dashboard')
    else:
        context = {
            'studentform': studentform,
        }
        return render(request, "createstudent.html", context)

def Logout(request):
    logout(request)
    return redirect("/")
