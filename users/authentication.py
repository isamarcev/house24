from django.contrib.auth.backends import BaseBackend, ModelBackend
from .models import CustomUser


def get_request_path(request):
    request_path_list = request.path.split('/')
    return request_path_list


class EmailAuthentication(BaseBackend):

    def authenticate(self, request, username=None, password=None, **kwargs):
        request_path_list = get_request_path(request)
        if username is None:
            username = kwargs.get(CustomUser.USERNAME_FIELD)
        if username is None or password is None:
            return
        try:
            user = CustomUser._default_manager.get(email=username)
            if user.role and request_path_list[3] == 'login':
                return None
            elif not user.role and request_path_list[3] == 'admin-login':
                return None
            else:
                return user
        except CustomUser.DoesNotExist:
            CustomUser().set_password(password)
            return None

    def get_user(self, user_id):
        try:
            return CustomUser.objects.get(pk=user_id)
        except CustomUser.DoesNotExist:
            return None


class IdAuthentication(ModelBackend):

    def authenticate(self, request, username=None, password=None, **kwargs):
        request_path_list = get_request_path(request)
        if username is None:
            username = kwargs.get(CustomUser.USERNAME_FIELD)
        if username is None or password is None:
            return
        try:
            user = CustomUser._default_manager.get_by_natural_key(username)
            if user.role and request_path_list[3] == 'login':
                return None
            elif not user.role and request_path_list[3] == 'admin-login':
                return None
            else:
                return user
        except CustomUser.DoesNotExist:
            CustomUser().set_password(password)



