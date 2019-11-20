from django import forms
from . import models
from .models import Quiz, QuizQuestion, QuizAnswer
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User

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
        fields = ('quiz_title', 'num_questions', 'grade_level',)

    quiz_title = forms.CharField(label="Quiz title")
    grade_level = forms.IntegerField(label="Grade level (0 = Kinder)", min_value=0, max_value=5)
    num_questions = forms.IntegerField(label="Number of questions", min_value=0)

class QuestionCreation(forms.ModelForm):
    class Meta:
        model = QuizQuestion
        fields = ('question_text',)
