# permissions.py

from rest_framework import permissions


class IsAdminOrReadOnly(permissions.BasePermission):
    """
    Custom permission to only allow admins to edit objects.
    Anyone can view, but only admins can edit.
    """

    def has_permission(self, request, view):
        # Read permissions are allowed to any request,
        # so we'll always allow GET, HEAD or OPTIONS requests.
        if request.method in permissions.SAFE_METHODS:
            return True

        # Write permissions are only allowed to admin users.
        return request.user and request.user.is_staff


class IsOwnerOrStaffOrReadOnly(permissions.BasePermission):
    """
    Custom permission to only allow owners of an object or staff to edit it.
    Anyone can view, but only owner or staff can edit.
    """

    def has_object_permission(self, request, view, obj):
        # Read permissions are allowed to any request,
        # so we'll always allow GET, HEAD or OPTIONS requests.
        if request.method in permissions.SAFE_METHODS:
            return True

        # Check if object has an owner field and if current user is owner
        if hasattr(obj, 'owner'):
            return obj.owner == request.user or request.user.is_staff
        # Check if object has a user field and if current user is that user
        elif hasattr(obj, 'user'):
            return obj.user == request.user or request.user.is_staff
        # If no user/owner field on the object, check if user is staff
        else:
            return request.user.is_staff


class IsEnrolledOrStaff(permissions.BasePermission):
    """
    Custom permission to only allow students enrolled in a course or staff to access it.
    """

    def has_object_permission(self, request, view, obj):
        # Staff can access everything
        if request.user.is_staff:
            return True
            
        # For courses, check if user is enrolled
        if hasattr(obj, 'students'):
            return request.user in obj.students.all()
            
        # For course-related objects, check if user is enrolled in the course
        if hasattr(obj, 'course') and hasattr(obj.course, 'students'):
            return request.user in obj.course.students.all()
            
        return False