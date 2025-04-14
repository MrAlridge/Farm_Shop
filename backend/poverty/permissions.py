from rest_framework import permissions

class IsSocialUser(permissions.BasePermission):
    """
    只允许普通用户（social）访问
    """
    def has_permission(self, request, view):
        return bool(
            request.user and 
            request.user.is_authenticated and 
            request.user.user_type == 'social'
        )

class IsOwnerOrAdmin(permissions.BasePermission):
    """
    允许管理员访问任何申请，普通用户只能访问自己的申请
    """
    def has_object_permission(self, request, view, obj):
        # 管理员可以访问任何对象
        if request.user.is_staff:
            return True
        # 普通用户只能访问自己的申请
        return obj.user == request.user

    def has_permission(self, request, view):
        return bool(request.user and request.user.is_authenticated) 