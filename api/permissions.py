from rest_framework import permissions

from account.models import User


class IsCashierPermission(permissions.BasePermission):

    def has_permission(self, request, view):
        if not bool(request.user and request.user.is_authenticated):
            return False
        try:
            return bool(request.user.is_cashier() and request.user.employee)
        except User.employee.RelatedObjectDoesNotExist as e:
            return False
