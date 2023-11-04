from rest_framework import status
from rest_framework.test import APITestCase

from course.models import Course, Lesson, Test, Question, Answer
from users.models import User


class LessonTestCase(APITestCase):

    def setUp(self) -> None:
        self.user = User.objects.create(
            email='test@test.com'
        )
        self.user.set_password('1234')
        self.user.save()

        self.course = Course.objects.create(school=1)

        self.lesson = Lesson.objects.create(
            owner=self.user,
            course=self.course,
            theme='TestLesson',
            description='TestLessonDescription',
            material='TestMaterialText',
        )

        self.test = Test.objects.create(
            lesson=self.lesson,
            title='TestForTestLesson',
            description='TestDescriptionForTest'
        )

        self.question = Question.objects.create(
            test=self.test,
            text='TestQuestion',
        )

        self.answer1 = Answer.objects.create(
            question=self.question,
            text='TestAnswer1',
            is_true=True
        )

        self.answer2 = Answer.objects.create(
            question=self.question,
            text='TestAnswer2',
            is_true=False
        )

    def test_create_lesson(self):
        """ Тестирование создания урока """
        data = {
            'theme': 'TestLesson2',
            'description': 'TestLessonDescription2',
            'material': 'TestMaterialText2',
            'course': self.course.pk
        }

        self.client.force_authenticate(user=self.user)
        response = self.client.post(
            '/lesson/create/',
            data=data
        )

        self.assertEquals(
            response.status_code,
            status.HTTP_201_CREATED
        )

        self.assertTrue(
            Lesson.objects.all().exists()
        )

        self.assertEqual(
            response.json(),
            {'course': 1, 'theme': 'TestLesson2', 'description': 'TestLessonDescription2',
             'material': 'TestMaterialText2', 'tests': []}
        )

    def test_list_lesson(self):
        """Тестирование вывода списка уроков"""
        self.client.force_authenticate(user=self.user)
        response = self.client.get(
            '/lesson/',
        )
        self.assertEqual(
            response.status_code,
            status.HTTP_200_OK
        )

        self.assertEqual(
            len(response.json()),
            1
        )

    def test_lesson_retrieve(self) -> None:
        self.client.force_authenticate(user=self.user)

        response = self.client.get(f'/lesson/{self.lesson.pk}/')

        self.assertEqual(
            response.status_code,
            status.HTTP_200_OK,
        )
        response = response.json()

        self.assertEqual(response.get('theme'), 'TestLesson')
        self.assertEqual(response.get('description'), 'TestLessonDescription')
        self.assertEqual(response.get('course'), self.course.pk)

    def test_lesson_update(self):
        self.client.force_authenticate(user=self.user)

        data = {
            'theme': 'TestLessonUpdated',
            'description': 'TestLessonDescriptionUpdated',
            'material': 'TestMaterialTextUpdated',
            'course': self.course.pk
        }

        response = self.client.put(
            path=f'/lesson/{self.lesson.pk}/update/', data=data,
        )

        self.assertEqual(
            response.status_code,
            status.HTTP_200_OK,
        )
        response = response.json()

        self.assertEqual(response.get('theme'), 'TestLessonUpdated')
        self.assertEqual(response.get('description'), 'TestLessonDescriptionUpdated')
        self.assertEqual(response.get('course'), self.course.pk)

    def test_lesson_delete(self):
        self.client.force_authenticate(user=self.user)

        response = self.client.delete(
            f'/lesson/{self.lesson.pk}/delete/',
        )

        self.assertEqual(
            response.status_code,
            status.HTTP_204_NO_CONTENT,
        )
        self.assertFalse(
            Lesson.objects.all().exists(),
        )

    def tearDown(self) -> None:
        self.user.delete()
        self.course.delete()
        self.lesson.delete()
        self.test.delete()
        self.question.delete()
        self.answer1.delete()
        self.answer2.delete()


class ResultTestCase(APITestCase):

    def setUp(self) -> None:
        self.user = User.objects.create(
            email='test@test.com'
        )
        self.user.set_password('1234')
        self.user.save()

        self.course = Course.objects.create(school=1)

        self.lesson = Lesson.objects.create(
            owner=self.user,
            course=self.course,
            theme='TestLesson',
            description='TestLessonDescription',
            material='TestMaterialText',
        )

        self.test = Test.objects.create(
            lesson=self.lesson,
            title='TestForTestLesson',
            description='TestDescriptionForTest'
        )

        self.question = Question.objects.create(
            test=self.test,
            text='TestQuestion',
        )

        self.answer1 = Answer.objects.create(
            question=self.question,
            text='TestAnswer1',
            is_true=True
        )

        self.answer2 = Answer.objects.create(
            question=self.question,
            text='TestAnswer2',
            is_true=False
        )

    def test_create_result(self):
        """Тестирование ответов на вопросы теста"""

        data = {
            'answer': self.answer1.pk,
        }

        self.client.force_authenticate(user=self.user)

        response = self.client.post(
            f'/question/{self.question.pk}/answer/',
            data=data
        )

        self.assertEquals(
            response.status_code,
            status.HTTP_200_OK
        )

        self.assertEqual(response.json().get('data'), {'answer': 11})
        self.assertEqual(response.json().get('result'), True)

    def tearDown(self) -> None:
        self.user.delete()
        self.course.delete()
        self.lesson.delete()
        self.test.delete()
        self.question.delete()
        self.answer1.delete()
        self.answer2.delete()


