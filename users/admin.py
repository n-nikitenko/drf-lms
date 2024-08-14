from django.contrib import admin

from users.models import Payment, User


@admin.register(User)
class UserAdmin(admin.ModelAdmin):
    list_display = (
        "email",
        "phone",
        "avatar",
        "is_active",
        "is_staff",
    )


@admin.register(Payment)
class PaymentAdmin(admin.ModelAdmin):
    list_display = ("user", "created_at", "course", "lesson", "value", "method")
