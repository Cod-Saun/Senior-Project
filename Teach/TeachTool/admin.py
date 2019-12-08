from django.contrib import admin
from . import models

# Register your models here.
admin.site.register(models.Quiz)
admin.site.register(models.QuizQuestion)
admin.site.register(models.QuizAnswer)
admin.site.register(models.Student)
admin.site.register(models.StudentAnswer)
admin.site.register(models.QuizResult)

