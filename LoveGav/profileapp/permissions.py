from rest_framework import permissions


class IsOwnerOrStaffReadOnly(permissions.BasePermission):
    """
    Пользовательское разрешение, позволяющее редактировать объект только его владельцу или административному персоналу
    """

    def has_object_permission(self, request, view, obj):
        if request.method in permissions.SAFE_METHODS:
            return True
        return obj == request.user or request.user.is_staff