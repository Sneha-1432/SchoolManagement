from rest_framework import permissions

class IsAdminUser(permissions.BasePermission):
    # Custom permission to only allow Admin users to access certain views.
    def has_permission(self,request, view):
        # Check if the user is authenticated 
        return request.user.is_authenticated and request.user.is_admin
    
class IsOfficeStaff(permissions.BasePermission):
    def has_permission(self, request, view):
        return request.user.is_authenticated and request.user.is_office_staff
    
class IsLibrarian(permissions.BasePermission):
    def has_permission(self, request, view):
        return request.user.is_authenticated and request.user.is_librarian
    
class IsAdminOrOfficeStaff(permissions.BasePermission):
    # Custom permission to allow access to both Admin and Office Staff users.
    def has_permission(self, request, view):
        return request.user.is_authenticated and (request.user.is_admin or request.user.is_office_staff)
    