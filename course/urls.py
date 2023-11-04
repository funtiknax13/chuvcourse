from django.urls import path

from course.apps import CourseConfig
from course.views import LessonListAPIView, LessonRetrieveAPIView, QuestionListAPIView, QuestionRetrieveAPIView, \
    ResultCreateAPIView, LessonCreateAPIView, LessonUpdateAPIView, LessonDestroyAPIView

app_name = CourseConfig.name


urlpatterns = [
    path('lesson/', LessonListAPIView.as_view(), name='lesson-list'),
    path('lesson/<int:pk>/', LessonRetrieveAPIView.as_view(), name='lesson-detail'),
    path('lesson/create/', LessonCreateAPIView.as_view(), name='lesson-create'),
    path('lesson/<int:pk>/update/', LessonUpdateAPIView.as_view(), name='lesson-update'),
    path('lesson/<int:pk>/delete/', LessonDestroyAPIView.as_view(), name='lesson-delete'),
    path('test/', QuestionListAPIView.as_view(), name='test-list'),
    path('test/<int:pk>/', QuestionRetrieveAPIView.as_view(), name='test-detail'),
    path('question/', QuestionListAPIView.as_view(), name='question-list'),
    path('question/<int:pk>/', QuestionRetrieveAPIView.as_view(), name='question-detail'),
    path('question/<int:pk>/answer/', ResultCreateAPIView.as_view(), name='question-answer'),
]
