from rest_framework.permissions import BasePermission


class RolePermission(BasePermission):
    def has_permission(self, request, view):
        user = request.user
        if not user.is_authenticated:
            return False

        if user.is_staff:
            return True

        required_roles = getattr(view, 'required_roles', [])
        token_role = request.auth.get('write')

        return token_role in required_roles
