from django.contrib.auth.models import Group
from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase

from materials.models import Course, Lesson, Subscription
from users.models import User


class LessonTestCase(APITestCase):
    """Тестирует CRUD занятий курса"""

    def setUp(self):
        self.user = User.objects.create(email="test_user@test.ru", password="testtest")
        self.moderator = User.objects.create(
            email="test_moderator@test.ru", password="testtest"
        )
        moderators_group = Group.objects.create(name="moderators")
        moderators_group.user_set.add(self.moderator)
        self.course = Course.objects.create(title="Test course", creator=self.user)
        self.lesson = Lesson.objects.create(
            title="Test lesson 1", course=self.course, creator=self.user
        )

    def test_lesson_retrieve(self):
        url = reverse("materials:lessons_retrieve", args=(self.lesson.pk,))
        self.client.force_authenticate(user=self.user)
        response = self.client.get(url)
        data = response.json()
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(data.get("title"), self.lesson.title)

    def test_lesson_list(self):
        url = reverse("materials:lessons_list")
        self.client.force_authenticate(user=self.moderator)
        response = self.client.get(url)
        data = response.json()
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(data.get("results")), Lesson.objects.count())

    def test_lesson_create(self):
        url = reverse("materials:lessons_create")
        self.client.force_authenticate(user=self.user)
        lesson_data = {
            "title": "Test lesson 2",
            "course": self.course.id,
            "creator": self.user.id,
        }
        response = self.client.post(url, data=lesson_data)
        data = response.json()
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(data.get("title"), lesson_data.get("title"))

    def test_lesson_update(self):
        url = reverse("materials:lessons_update", args=(self.lesson.pk,))
        self.client.force_authenticate(user=self.user)
        lesson_data = {"title": "Test lesson 3"}
        response = self.client.patch(url, data=lesson_data)
        data = response.json()
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(data.get("title"), lesson_data.get("title"))

    def test_lesson_delete(self):
        self.client.force_authenticate(user=self.user)
        url = reverse("materials:lessons_destroy", args=(self.lesson.pk,))
        response = self.client.delete(url)
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertEqual(Lesson.objects.count(), 0)


class CourseTestCase(APITestCase):
    """Тестирует CRUD курсов"""

    def setUp(self):
        self.user = User.objects.create(email="test_user@test.ru", password="testtest")
        self.moderator = User.objects.create(
            email="test_moderator@test.ru", password="testtest"
        )
        moderators_group = Group.objects.create(name="moderators")
        moderators_group.user_set.add(self.moderator)
        self.course = Course.objects.create(title="Test course", creator=self.user)

    def test_course_retrieve(self):
        url = reverse("materials:course-detail", args=(self.course.pk,))
        self.client.force_authenticate(user=self.user)
        response = self.client.get(url)
        data = response.json()
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(data.get("title"), self.course.title)

    def test_course_list(self):
        url = reverse("materials:course-list")
        self.client.force_authenticate(user=self.moderator)
        response = self.client.get(url)
        data = response.json()
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(data.get("results")), Course.objects.count())

    def test_course_create(self):
        url = reverse("materials:course-list")
        self.client.force_authenticate(user=self.user)
        course_data = {"title": "Test Course 2", "creator": self.user.id}
        response = self.client.post(url, data=course_data)
        data = response.json()
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(data.get("title"), course_data.get("title"))

    def test_course_update(self):
        url = reverse("materials:course-detail", args=(self.course.pk,))
        self.client.force_authenticate(user=self.user)
        course_data = {"title": "Test course 3"}
        response = self.client.patch(url, data=course_data)
        data = response.json()
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(data.get("title"), course_data.get("title"))

    def test_lesson_delete(self):
        self.client.force_authenticate(user=self.user)
        url = reverse("materials:course-detail", args=(self.course.pk,))
        response = self.client.delete(url)
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertEqual(Course.objects.count(), 0)


class SubscriptionTestCase(APITestCase):
    """Тестирует создание и удаление подписки пользователя на курс"""

    def setUp(self):
        self.user = User.objects.create(email="test_user@test.ru", password="testtest")
        self.course = Course.objects.create(title="Test course", creator=self.user)
        self.client.force_authenticate(user=self.user)

    def test_subscription_creating(self):
        url = reverse("materials:subscriptions")

        subscription_data = {"course": self.course.id}
        response = self.client.post(url, data=subscription_data)
        data = response.json()
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(data.get("message"), "подписка добавлена")

    def test_subscription_deleting(self):
        url = reverse("materials:subscriptions")

        subscription_data = {"course": self.course.id}
        Subscription.objects.create(course=self.course, user=self.user)

        response = self.client.post(url, data=subscription_data)
        data = response.json()
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(data.get("message"), "подписка удалена")
