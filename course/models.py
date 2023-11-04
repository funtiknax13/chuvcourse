from django.conf import settings
from django.db import models

from users.models import User

NULLABLE = {'null': True, 'blank': True}


class Course(models.Model):
    SCHOOL_CHOICE = [
        (1, 'Первый класс'),
        (2, 'Второй класс'),
        (3, 'Третий класс'),
        (4, 'Четвёртый класс'),
        (5, 'Пятый класс'),
        (6, 'Шестой класс'),
        (7, 'Седьмой класс'),
        (8, 'Восьмой класс'),
        (9, 'Девятый класс'),
        (10, 'Десятый класс'),
        (11, 'Одиннадцатый класс'),
    ]

    school = models.IntegerField(choices=SCHOOL_CHOICE, verbose_name='Класс', unique=True)

    def __str__(self):
        return f'{self.school} класс'

    class Meta:
        verbose_name = 'Класс'
        verbose_name_plural = 'Классы'


class Lesson(models.Model):
    owner = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, **NULLABLE)
    course = models.ForeignKey(Course, on_delete=models.CASCADE, verbose_name='класс')
    theme = models.CharField(max_length=300, verbose_name='тема урока')
    description = models.TextField(verbose_name='описание урока')
    material = models.TextField(verbose_name='материал урока')

    def __str__(self):
        return self.theme

    class Meta:
        verbose_name = 'Урок'
        verbose_name_plural = 'Уроки'


class Test(models.Model):
    lesson = models.ForeignKey(Lesson, on_delete=models.CASCADE, verbose_name='урок')
    title = models.CharField(max_length=300, verbose_name='название теста')
    description = models.TextField(verbose_name='описание теста', **NULLABLE)

    def __str__(self):
        return self.title

    class Meta:
        verbose_name = 'Тест'
        verbose_name_plural = 'Тесты'


class Question(models.Model):
    test = models.ForeignKey(Test, on_delete=models.CASCADE, verbose_name='тест')
    text = models.CharField(max_length=300, verbose_name='текст вопроса')

    def __str__(self):
        return self.text

    class Meta:
        verbose_name = 'Вопрос'
        verbose_name_plural = 'Вопросы'


class Answer(models.Model):
    question = models.ForeignKey(Question, on_delete=models.CASCADE, verbose_name='вопрос')
    text = models.CharField(max_length=300, verbose_name='текст ответа')
    is_true = models.BooleanField(default=False, verbose_name='признак правильности ответа')

    def __str__(self):
        return self.text

    class Meta:
        verbose_name = 'Ответ'
        verbose_name_plural = 'Ответы'


class Result(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, verbose_name='пользователь')
    question = models.ForeignKey(Question, on_delete=models.CASCADE, verbose_name='вопрос')
    answer = models.ForeignKey(Answer, on_delete=models.CASCADE, verbose_name='ответ пользователя')

    def __str__(self):
        return f'{self.user.email} на вопрос "{self.question.text}" дал ответ "{self.answer.text}"'

    class Meta:
        verbose_name = 'Ответ пользователя'
        verbose_name_plural = 'Ответы пользователя'

