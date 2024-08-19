from rest_framework import permissions


class IsModeratorPermission(permissions.BasePermission):
    """проверка, является ли пользователь модератором."""

    def has_permission(self, request, view):
        return request.user.is_moderator


class IsOwnerPermission(permissions.BasePermission):
    """проверка, является ли пользователь автором материала."""

    def has_object_permission(self, request, view, obj):
        return obj.creator == request.user
