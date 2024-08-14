from django.shortcuts import render
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.filters import OrderingFilter
from rest_framework.generics import ListAPIView

from users.models import Payment
from users.serializers import PaymentSerializer


class PaymentListApiView(ListAPIView):
    """список платежей"""

    serializer_class = PaymentSerializer
    queryset = Payment.objects.all()
    filter_backends = (DjangoFilterBackend, OrderingFilter)
    filterset_fields = ("course", "lesson", "method")
    ordering_fields = ("created_at",)
