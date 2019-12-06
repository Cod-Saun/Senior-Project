from django import forms
from . import models
from .models import Quiz, QuizQuestion, QuizAnswer, Student
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from django.forms import ModelChoiceField

class RegistrationForm(UserCreationForm):
    email = forms.EmailField(
        label="Email",
        required=True
    )

    class Meta:
        model = User
        fields = ('username', 'email', 'password1', 'password2',)

    def save(self, commit=True):
        user = super(RegistrationForm, self).save(commit=False)
        user.email = self.cleaned_data["email"]
        if commit:
            user.save()
        return user

class QuizCreation(forms.ModelForm):
    class Meta:
        model = Quiz
        fields = ('quiz_title', 'num_questions', 'grade_level', 'subject', 'summary',)

    quiz_title = forms.CharField(label="Quiz title")
    grade_level = forms.IntegerField(label="Grade level (0 = Kinder)", min_value=0, max_value=5)
    num_questions = forms.IntegerField(label="Number of questions", min_value=0)

class QuestionCreation(forms.ModelForm):
    class Meta:
        model = QuizQuestion
        fields = ('question_text',)

class StudentCreation(forms.ModelForm):
    class Meta:
        model = Student
        fields = ('first_name', 'last_name', 'grade_level',)

    first_name = forms.CharField(label="First Name")
    last_name = forms.CharField(label="Last Name")
    grade_level = forms.IntegerField(label="Grade level (0 = Kinder)", min_value=0, max_value=5)

class SelectAnswer(forms.Form):
    class Meta:
        model = QuizAnswer
        fields = ("answer_text",)
    
    answer_text = forms.ModelChoiceField(queryset=QuizAnswer.objects.all(), widget=forms.RadioSelect(), empty_label=None, required=True, label='')

class StudentNames(ModelChoiceField):
    def label_from_instance(self, obj):
        return '{firstname} {lastname}'.format(firstname=obj.first_name, lastname=obj.last_name)

class SelectStudent(forms.Form):
    students = StudentNames(queryset=Student.objects.all(), empty_label=None, required=True, label="Select a Student")