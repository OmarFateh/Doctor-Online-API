from rest_framework import permissions


class IsDoctor(permissions.BasePermission):
    """
    A custom permission to allow only doctors to view/create an object.
    """
    message = "You have to be a doctor to apply action for this item."

    def has_permission(self, request, view):
        # User must be a doctor.
        if request.user.is_authenticated:
            return request.user.user_type == 'D'
        return False 


class IsDoctorOwner(IsDoctor):
    """
    Object-level permission to allow only the doctor of clinic to edit/delete it.
    """
    message = "You have to be the doctor of this clinic to apply action for this item."

    # def has_permission(self, request, view):
    #     # User must be a doctor.
    #     if request.user.is_authenticated:
    #         return request.user.user_type == 'D'
    #     return False 

    def has_object_permission(self, request, view, obj):
        return obj.doctor == request.user.doctor


class IsDoctorOwnerOrReadOnly(permissions.BasePermission):
    """
    Object-level permission to allow only the doctor of clinic to edit/delete it.
    Otherwise it will be displayed only for authenticated users.
    """
    message = "You have to be the doctor of this clinic to apply action for this item."

    def has_permission(self, request, view):
        # User must be authenticated.
        return request.user.is_authenticated 

    def has_object_permission(self, request, view, obj):
        # it always allow GET, HEAD or OPTIONS requests.
        if request.method in permissions.SAFE_METHODS:
            return True
        if request.user.user_type == 'D':    
            return obj.doctor == request.user.doctor
        return False    