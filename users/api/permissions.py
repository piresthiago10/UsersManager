from rest_framework import permissions
from users.models import User

class IsSameDepartmentOrStaff(permissions.BasePermission):

    def has_permission(self, request, obj):
        """Checks whether the logged in user is a staff member
        or is in the same department as the user he is trying to modify.

        Returns:
            boolean: True if the condition values ​​are the same
        """
        try:
            obj_user_department = User.objects.get(id=obj.kwargs['pk'])
        except obj_user_department.DoesNotExist:
            return False

        user_department_id = request.user.department_id
        obj_user_department_pk = obj_user_department.department.pk
        
        if user_department_id == obj_user_department_pk or request.user.is_staff:
            return True
        return False

class IsOwnProfileOrStaff(permissions.BasePermission):
    
    def has_permission(self, request, obj):
        """Checks if the logged in user has the same object id.

        Returns:
            boolean: True if the condition values ​​are the same
        """
        try:
            obj_user = User.objects.get(id=obj.kwargs['pk'])
        except obj_user.DoesNotExist:
            return False
        
        user_pk = request.user.pk
        obj_pk = obj_user.pk
        if user_pk == obj_pk or request.user.is_staff:
            return True
        return False