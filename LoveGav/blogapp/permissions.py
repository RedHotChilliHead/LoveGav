from rest_framework import permissions


class IsAuthorOrReadOnly(permissions.BasePermission):
    """
    Пользовательское разрешение, позволяющее редактировать объект только его авторам
    """

    def has_object_permission(self, request, view, obj):
        if request.method in permissions.SAFE_METHODS:
            return True
        return obj.author == request.user