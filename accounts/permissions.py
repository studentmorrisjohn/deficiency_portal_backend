from accounts.models import User
from rest_framework import permissions

def is_in_group(user, group_name):
    try:
        return User.objects.get(pk=user.id).groups.filter(name=group_name)
    except User.DoesNotExist:
        return False


class HasEmployeePermission(permissions.BasePermission):
    def has_permission(self, request, view):
        try:
            return request.user.role == "EMPLOYEE" or request.user.role == "ADMIN"
        except AttributeError:
            return False

class HasOwnerPermission(permissions.BasePermission):
    def has_permissions(self, request, view):
        return