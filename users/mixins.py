from django.contrib.auth.mixins import LoginRequiredMixin, \
    UserPassesTestMixin
from django.shortcuts import redirect
from django.urls import reverse_lazy
from django.contrib import messages
from task_manager.messages import NO_USER_PERMISSION_MESSAGE,\
    NO_AUTHORIZATION_MESSAGE


class MyLoginRequiredMixin(LoginRequiredMixin):
    redirect_field_name = reverse_lazy('login')

    # def dispatch(self, request, *args, **kwargs):
    #     messages.warning(self.request, NO_AUTHORIZATION_MESSAGE)
    #     return super().dispatch(request, *args, **kwargs)

    def handle_no_permission(self):
        messages.warning(self.request, NO_AUTHORIZATION_MESSAGE)
        url = reverse_lazy('login')
        return redirect(url)


class UserPermissionMixin(UserPassesTestMixin):
    def test_func(self):
        user = self.get_object()
        return self.request.user.id == user.id

    def handle_no_permission(self):
        messages.warning(self.request, NO_USER_PERMISSION_MESSAGE)
        url = reverse_lazy('users:users')
        return redirect(url)
