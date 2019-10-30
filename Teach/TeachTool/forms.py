from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User

class RegistrationForm(UserCreationForm):
    email = forms.EmailField(
        label="Email",
        required=True
    )

    class Meta:
        model = User
        fields = ("username", "email", "password1", "password2")

    def save(self, commit=True):
        user = super(RegistrationForm, self).save(commit=False)
        user.email = self.cleaned_data["email"]
        if commit:
            user.save()
        return user

class QuizCreation(forms.Form):
    questions = []
    quiz_title = forms.CharField(label="Quiz Title")
    num_questions = forms.IntegerField(label="Number of questions")
    question = forms.CharField(label="Question 1", widget=forms.Textarea)

