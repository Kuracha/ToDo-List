from rest_framework.permissions import BasePermission


class IsOwnerOrReadOnly(BasePermission):
    message = 'Only owners can change task status'

    def has_object_permission(self, request, view, obj):
        return obj.creator == request.user
