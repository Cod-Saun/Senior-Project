# Generated by Django 2.2.5 on 2019-11-12 06:02

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('TeachTool', '0001_initial'),
    ]

    operations = [
        migrations.RenameModel(
            old_name='Quizzes',
            new_name='Quiz',
        ),
        migrations.RenameModel(
            old_name='QuizAnswers',
            new_name='QuizAnswer',
        ),
        migrations.RenameModel(
            old_name='QuizQuestions',
            new_name='QuizQuestion',
        ),
    ]