from django.db import models
from django.contrib.auth.models import User

# Create your models here.
class Quiz(models.Model):
    quiz_id = models.AutoField(primary_key=True)
    quiz_title = models.CharField(max_length=50)
    num_questions = models.IntegerField()
    grade_level = models.IntegerField()

class QuizQuestion(models.Model):
    question_id = models.AutoField(primary_key=True)
    quiz_id = models.ForeignKey(Quiz, on_delete=models.CASCADE, default=1)
    question_text = models.CharField(max_length=1000)

class QuizAnswer(models.Model):
    answer_id = models.AutoField(primary_key=True)
    question_id = models.ForeignKey(QuizQuestion, on_delete=models.CASCADE, default=1)
    answer_text = models.CharField(max_length=1000)
    is_correct = models.BooleanField()