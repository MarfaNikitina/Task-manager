from django.contrib.auth.mixins import LoginRequiredMixin, \
    UserPassesTestMixin
from django.shortcuts import redirect
from django.urls import reverse_lazy

from task_manager import messages
from task_manager.messages import NO_USER_PERMISSION_MESSAGE, NO_AUTHORIZATION_MESSAGE


class UserPermissionMixin(LoginRequiredMixin, UserPassesTestMixin):
    def test_func(self):
        user = self.get_object()
        return self.request.user.id == user.id

    def handle_no_permission(self):
        if self.request.user.is_authenticated:
            messages.warning(self.request, NO_USER_PERMISSION_MESSAGE)
            url = reverse_lazy('users:users')
        else:
            url = self.login_url
            messages.warning(self.request, NO_AUTHORIZATION_MESSAGE)
        return redirect(url)