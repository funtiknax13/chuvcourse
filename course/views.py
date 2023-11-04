from rest_framework import viewsets, generics
from rest_framework.exceptions import ValidationError
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.filters import OrderingFilter

from course.models import Course, Lesson, Question, Answer, Result, Test
from course.permissions import IsOwner
from course.serializers import QuestionSerializer, LessonSerializer, ResultSerializer, TestSerializer


class LessonCreateAPIView(generics.CreateAPIView):
    serializer_class = LessonSerializer
    permission_classes = [IsAuthenticated, ]

    def perform_create(self, serializer):
        new_lesson = serializer.save()
        new_lesson.owner = self.request.user
        new_lesson.save()


class LessonListAPIView(generics.ListAPIView):
    serializer_class = LessonSerializer
    queryset = Lesson.objects.all()
    permission_classes = [IsAuthenticated, ]
    filter_backends = [DjangoFilterBackend, OrderingFilter]
    filterset_fields = ('course', )
    ordering_fields = ('course', )


class LessonRetrieveAPIView(generics.RetrieveAPIView):
    serializer_class = LessonSerializer
    queryset = Lesson.objects.all()
    permission_classes = [IsAuthenticated, ]


class LessonUpdateAPIView(generics.UpdateAPIView):
    serializer_class = LessonSerializer
    queryset = Lesson.objects.all()
    permission_classes = [IsAuthenticated, IsOwner]


class LessonDestroyAPIView(generics.DestroyAPIView):
    queryset = Lesson.objects.all()
    permission_classes = [IsAuthenticated, IsOwner]


class TestListAPIView(generics.ListAPIView):
    serializer_class = TestSerializer
    queryset = Test.objects.all()
    permission_classes = [IsAuthenticated, ]


class TestRetrieveAPIView(generics.RetrieveAPIView):
    serializer_class = TestSerializer
    queryset = Test.objects.all()
    permission_classes = [IsAuthenticated, ]


class QuestionListAPIView(generics.ListAPIView):
    serializer_class = QuestionSerializer
    queryset = Question.objects.all()
    permission_classes = [IsAuthenticated, ]


class QuestionRetrieveAPIView(generics.RetrieveAPIView):
    serializer_class = QuestionSerializer
    queryset = Question.objects.all()
    permission_classes = [IsAuthenticated, ]


class ResultCreateAPIView(generics.CreateAPIView):
    serializer_class = ResultSerializer
    permission_classes = [IsAuthenticated, ]

    def perform_create(self, serializer, *args, **kwargs):
        question = Question.objects.get(id=self.kwargs.get('pk'))
        user = self.request.user
        answer = serializer.validated_data.get('answer')
        answers = question.answer_set.all()

        if answer not in answers:
            raise ValidationError({'error': 'The answer does not exist'})

        if Result.objects.filter(user=user, question=question).exists():
            raise ValidationError({'error': 'This question has already been answered'})

        serializer.save(user=user, question=question)

    def create(self, request, *args, **kwargs):
        response = super().create(request, *args, **kwargs)
        user_answer = Answer.objects.get(id=response.data["answer"])

        return Response({
            'data': response.data,
            'result': user_answer.is_true
        })
