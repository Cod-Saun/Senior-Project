# Generated by Django 2.2.5 on 2019-11-24 07:11

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('TeachTool', '0005_auto_20191124_0627'),
    ]

    operations = [
        migrations.CreateModel(
            name='Student',
            fields=[
                ('student_id', models.AutoField(primary_key=True, serialize=False)),
                ('first_name', models.CharField(max_length=50)),
                ('last_name', models.CharField(max_length=50)),
                ('grade_level', models.IntegerField()),
            ],
        ),
    ]
