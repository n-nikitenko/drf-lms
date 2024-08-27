from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.exceptions import ValidationError
from rest_framework.filters import OrderingFilter
from rest_framework.generics import (CreateAPIView, DestroyAPIView,
                                     ListAPIView, RetrieveAPIView,
                                     UpdateAPIView)
from rest_framework.permissions import AllowAny

from users.models import Payment, User
from users.serializers import (PaymentCreateSerializer, PaymentSerializer,
                               UserRetrieveSerializer, UserSerializer,
                               UserUpdateSerializer)
from users.services import (create_stripe_price, create_stripe_product,
                            create_stripe_session)


class PaymentListApiView(ListAPIView):
    """список платежей"""

    serializer_class = PaymentSerializer
    queryset = Payment.objects.all()
    filter_backends = (DjangoFilterBackend, OrderingFilter)
    filterset_fields = ("course", "lesson", "method")
    ordering_fields = ("created_at",)


class PaymentCreateApiView(CreateAPIView):
    """Cоздание платежа за курс или занятие, сумма (value) указывается в копейках.
    Нужно указать курс (course) или занятие (lesson)"""

    serializer_class = PaymentCreateSerializer
    queryset = Payment.objects.all()

    def perform_create(self, serializer):
        payment = serializer.save(user=self.request.user)

        if payment.course:
            product_name = f'Курс "{payment.course.title}"'
        elif payment.lesson:
            product_name = f'Занятие "{payment.lesson.title}"'
        else:
            raise ValidationError("Нужно указать курс или занятие")
        stripe_product = create_stripe_product(product_name)
        stripe_price = create_stripe_price(payment.value, stripe_product.get("id"))
        payment.session_id, payment.link = create_stripe_session(stripe_price.get("id"))
        payment.save()


class UserCreateApiView(CreateAPIView):
    """создание пользователя"""

    serializer_class = UserSerializer
    queryset = User.objects.all()
    permission_classes = [AllowAny]

    def perform_create(self, serializer):
        user = serializer.save(is_active=True)
        user.set_password(user.password)
        user.save()


class UserRetrieveApiView(RetrieveAPIView):
    serializer_class = UserRetrieveSerializer
    queryset = User.objects.all()


class UserListApiView(ListAPIView):
    serializer_class = UserRetrieveSerializer
    queryset = User.objects.all()


class UserUpdateApiView(UpdateAPIView):
    serializer_class = UserUpdateSerializer
    queryset = User.objects.all()


class UserDestroyApiView(DestroyAPIView):
    serializer_class = UserUpdateSerializer
    queryset = User.objects.all()
