from django.utils.decorators import method_decorator
from drf_yasg.utils import swagger_auto_schema
from rest_framework import status
from rest_framework.generics import (CreateAPIView, DestroyAPIView,
                                     ListAPIView, RetrieveAPIView,
                                     UpdateAPIView)
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.viewsets import ModelViewSet

from materials.models import Course, Lesson, Subscription
from materials.paginators import MaterialPaginator
from materials.permissions import IsModeratorPermission, IsOwnerPermission
from materials.serializers import (CourseSerializer, LessonSerializer,
                                   SubscriptionSerializer)


@method_decorator(
    name="list",
    decorator=swagger_auto_schema(operation_description="Получение списка курсов"),
)
@method_decorator(
    name="create", decorator=swagger_auto_schema(operation_description="Создание курса")
)
@method_decorator(
    name="retrieve",
    decorator=swagger_auto_schema(operation_description="Получение данных курса по id"),
)
@method_decorator(
    name="update",
    decorator=swagger_auto_schema(
        operation_description="Обновление данных курса по id"
    ),
)
@method_decorator(
    name="destroy",
    decorator=swagger_auto_schema(operation_description="Удаление курса по id"),
)
class CourseViewSet(ModelViewSet):
    queryset = Course.objects.all()
    serializer_class = CourseSerializer
    pagination_class = MaterialPaginator

    def perform_create(self, serializer):
        serializer.save(creator=self.request.user)

    def get_permissions(self):
        if self.action == "create":
            self.permission_classes = (
                IsAuthenticated,
                ~IsModeratorPermission,
            )
        elif self.action == "destroy":
            self.permission_classes = (
                IsAuthenticated,
                ~IsModeratorPermission | IsOwnerPermission,
            )
        self.permission_classes = (
            IsAuthenticated,
            IsModeratorPermission | IsOwnerPermission,
        )
        return super().get_permissions()


class LessonCreateApiView(CreateAPIView):
    """Создание занятия"""

    serializer_class = LessonSerializer
    queryset = Lesson.objects.all()
    permission_classes = (
        IsAuthenticated,
        ~IsModeratorPermission,
    )

    def perform_create(self, serializer):
        serializer.save(creator=self.request.user)


class LessonRetrieveApiView(RetrieveAPIView):
    """Получение данных занятия по id"""

    serializer_class = LessonSerializer
    queryset = Lesson.objects.all()
    permission_classes = (
        IsAuthenticated,
        IsModeratorPermission | IsOwnerPermission,
    )


class LessonListApiView(ListAPIView):
    """Получение списка занятий"""

    serializer_class = LessonSerializer
    pagination_class = MaterialPaginator
    queryset = Lesson.objects.all()
    permission_classes = (IsAuthenticated, IsModeratorPermission)


class LessonUpdateApiView(UpdateAPIView):
    """Обновление данных занятия"""

    serializer_class = LessonSerializer
    queryset = Lesson.objects.all()
    permission_classes = (
        IsAuthenticated,
        IsModeratorPermission | IsOwnerPermission,
    )


class LessonDestroyApiView(DestroyAPIView):
    """Удаление занятия по id"""

    serializer_class = LessonSerializer
    queryset = Lesson.objects.all()
    permission_classes = (
        IsAuthenticated,
        ~IsModeratorPermission | IsOwnerPermission,
    )


class SubscriptionViewSet(APIView):
    queryset = Subscription.objects.all()
    serializer_class = SubscriptionSerializer

    def post(self, request, format=None):
        """Если подписка текущего пользователя на указанный курс существует, удалить. Иначе - создать."""

        serializer = self.serializer_class(data=request.data)
        if serializer.is_valid():
            course_item = serializer.validated_data.get("course")
            subs_item = Subscription.objects.filter(
                course=course_item, user=request.user
            )
            if subs_item.exists():
                message = "подписка удалена"
                subs_item.delete()
                status_code = status.HTTP_200_OK
            else:
                message = "подписка добавлена"
                status_code = status.HTTP_201_CREATED
                serializer.validated_data["user"] = request.user
                serializer.save()
            return Response(
                {"message": message, "data": serializer.data}, status=status_code
            )
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
