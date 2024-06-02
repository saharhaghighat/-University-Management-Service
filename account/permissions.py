from rest_framework.permissions import BasePermission
from rest_framework.permissions import IsAuthenticated

from samane_golestan.settings import ASSISTANTS_GROUP_NAME


class IsAdmin(BasePermission):
    def has_permission(self, request, view):
        user = request.user
        return (
            IsAuthenticated and
            user.is_superuser
        )


class IsEducationalAssistant(BasePermission):
    def has_permission(self, request, view):
        user = request.user
        return (
            IsAuthenticated and
            user.groups.filter(name=ASSISTANTS_GROUP_NAME).exists()
        )
