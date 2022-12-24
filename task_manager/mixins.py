from django.contrib.auth.mixins import LoginRequiredMixin, \
    UserPassesTestMixin
from django.shortcuts import redirect
from django.urls import reverse_lazy
from django.contrib import messages
from task_manager.messages import NO_USER_PERMISSION_MESSAGE, \
    NO_AUTHORIZATION_MESSAGE, NO_DELETE_TASK_MESSAGE


class MyLoginRequiredMixin(LoginRequiredMixin):

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


class TaskPassesTestMixin(UserPassesTestMixin):
    def test_func(self):
        return self.get_object().author == self.request.user

    def handle_no_permission(self):
        url = reverse_lazy('tasks')
        messages.warning(self.request, NO_DELETE_TASK_MESSAGE)
        return redirect(url)
