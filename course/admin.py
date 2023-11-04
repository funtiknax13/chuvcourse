from django.contrib import admin

from course.models import Course, Lesson, Question, Answer, Result, Test

# Register your models here.
admin.site.register(Course)
admin.site.register(Lesson)
admin.site.register(Test)
admin.site.register(Question)
admin.site.register(Answer)
admin.site.register(Result)
