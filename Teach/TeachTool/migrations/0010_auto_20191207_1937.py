# Generated by Django 2.2.5 on 2019-12-07 19:37

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('TeachTool', '0009_auto_20191207_1932'),
    ]

    operations = [
        migrations.AlterField(
            model_name='studentanswer',
            name='quiz_id',
            field=models.ForeignKey(default=85, on_delete=django.db.models.deletion.CASCADE, to='TeachTool.Quiz'),
        ),
    ]
