# Generated by Django 2.2.5 on 2019-11-14 02:23

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('TeachTool', '0003_quizquestion_quiz_id'),
    ]

    operations = [
        migrations.AddField(
            model_name='quizanswer',
            name='question_id',
            field=models.ForeignKey(default=1, on_delete=django.db.models.deletion.CASCADE, to='TeachTool.QuizQuestion'),
        ),
    ]
