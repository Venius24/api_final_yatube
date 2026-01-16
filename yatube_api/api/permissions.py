from rest_framework import permissions


class IsAuthorOrReadOnly(permissions.BasePermission):
    def has_object_permission(self, request, view, obj):
        # Разрешаем GET, HEAD, OPTIONS
        if request.method in permissions.SAFE_METHODS:
            return True
        # Разрешаем изменения только автору
        return obj.author == request.user
    
    # Добавьте это, чтобы аноним получал 401, а не 403
    def has_permission(self, request, view):
        return (
            request.method in permissions.SAFE_METHODS
            or request.user.is_authenticated
        )