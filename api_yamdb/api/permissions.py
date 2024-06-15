from rest_framework import permissions


class IsAdminOrReadOnly(permissions.BasePermission):
    """
    Права на выполнение любых действий для администратора
    и просмотр для всех пользователей.
    """

    def has_permission(self, request, view):
        return (
            request.method in permissions.SAFE_METHODS
            or request.user.is_authenticated
            and request.user.is_admin
        )


class IsAllowedToEditOrReadOnly(permissions.BasePermission):
    """Права на редактирование всем кроме анонима."""

    def has_permission(self, request, view):
        return (
            request.method in permissions.SAFE_METHODS
            or request.user.is_authenticated
        )

    def has_object_permission(self, request, view, obj):
        return (
            request.method in permissions.SAFE_METHODS
            or obj.author == request.user
            or request.user.is_admin
            or request.user.is_moderator
        )


class IsAdmin(permissions.BasePermission):
    """
    Права на выполнение любых запросов для суперпользователя и администартора.
    """
    def has_permission(self, request, view):
        return (
            request.user.is_authenticated
            and request.user.is_admin
        )
