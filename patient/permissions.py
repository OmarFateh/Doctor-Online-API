from rest_framework import permissions


class IsPatient(permissions.BasePermission):
    """
    A custom permission to allow only patients to view/create an object.
    """
    message = "You have to be a patient to apply action for this item."

    def has_permission(self, request, view):
        # User must be a patient.
        if request.user.is_authenticated:
            return request.user.user_type == 'P'
        return False 