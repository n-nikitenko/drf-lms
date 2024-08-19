from rest_framework.generics import (CreateAPIView, DestroyAPIView,
                                     ListAPIView, RetrieveAPIView,
                                     UpdateAPIView)
from rest_framework.viewsets import ModelViewSet

from materials.models import Course, Lesson
from materials.serializers import CourseSerializer, LessonSerializer
from users.permissions import IsModeratorPermission


class CourseViewSet(ModelViewSet):
    queryset = Course.objects.all()
    serializer_class = CourseSerializer

    def perform_create(self, serializer):
        serializer.save(creator=self.request.user)

    def get_permissions(self):
        if self.action in ['create', 'destroy']:
            self.permission_classes = (~IsModeratorPermission,)
        self.permission_classes = (IsModeratorPermission,)
        return super().get_permissions()


class LessonCreateApiView(CreateAPIView):
    serializer_class = LessonSerializer
    queryset = Lesson.objects.all()
    permission_classes = (~IsModeratorPermission,)

    def perform_create(self, serializer):
        serializer.save(creator=self.request.user)


class LessonRetrieveApiView(RetrieveAPIView):
    serializer_class = LessonSerializer
    queryset = Lesson.objects.all()
    permission_classes = (IsModeratorPermission,)


class LessonListApiView(ListAPIView):
    serializer_class = LessonSerializer
    queryset = Lesson.objects.all()
    permission_classes = (IsModeratorPermission,)


class LessonUpdateApiView(UpdateAPIView):
    serializer_class = LessonSerializer
    queryset = Lesson.objects.all()
    permission_classes = (IsModeratorPermission,)


class LessonDestroyApiView(DestroyAPIView):
    serializer_class = LessonSerializer
    queryset = Lesson.objects.all()
    permission_classes = (~IsModeratorPermission,)
