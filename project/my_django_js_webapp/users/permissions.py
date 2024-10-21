from rest_framework.permissions import BasePermission

class CanAddPost(BasePermission):
    def has_permission(self, request, view):
        # POST 요청에 대해서만 권한을 검사
        if request.method == 'POST':
            # 사용자가 'add_post' 권한을 가지고 있는지 확인
            return request.user.has_perm('boards.add_post')
        return False

class IsInAdminGroup(BasePermission):
    """
    Admin 그룹에 속한 사용자 또는 슈퍼유저/스태프에게만 접근을 허용합니다.
    """
    def has_permission(self, request, view):
        return request.user and (request.user.is_staff or request.user.is_superuser or request.user.groups.filter(name='admin').exists())

class IsInEditorGroup(BasePermission):
    """
    Editor 그룹에 속한 사용자에게만 접근을 허용합니다.
    """
    def has_permission(self, request, view):
        return request.user and request.user.groups.filter(name='editor').exists()

class IsInUserGroup(BasePermission):
    """
    User 그룹에 속한 사용자에게만 접근을 허용합니다.
    """
    def has_permission(self, request, view):
        return request.user and request.user.groups.filter(name='user').exists()

