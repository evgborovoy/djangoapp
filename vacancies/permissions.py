from rest_framework import permissions

from authentication.models import User


class VacancyCreatePermission(permissions.BasePermission):
    message = "You don`t have a permission to create vacancy"

    def has_permission(self, request, view):
        if request.user.role == User.HR:
            return True
        return False