from rest_framework import serializers

from course.models import Course, Lesson, Question, Answer, Result, Test
from course.validators import AnswerValidator


class CourseSerializer(serializers.ModelSerializer):

    class Meta:
        model = Course
        fields = ['School', ]


class AnswerSerializer(serializers.ModelSerializer):

    class Meta:
        model = Answer
        fields = ['id', 'text', ]


class QuestionSerializer(serializers.ModelSerializer):

    answers = AnswerSerializer(source='answer_set', read_only=True, many=True)

    class Meta:
        model = Question
        fields = ['text', 'answers']


class TestSerializer(serializers.ModelSerializer):

    questions = QuestionSerializer(source='question_set', read_only=True, many=True)

    class Meta:
        model = Test
        fields = ['title', 'description', 'questions']


class LessonSerializer(serializers.ModelSerializer):

    tests = TestSerializer(source='test_set', read_only=True, many=True)

    class Meta:
        model = Lesson
        fields = ['course', 'theme', 'description', 'material', 'tests']


class ResultSerializer(serializers.ModelSerializer):

    class Meta:
        model = Result
        fields = ['answer']
        validators = [AnswerValidator(), ]
