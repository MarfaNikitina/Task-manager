from django.contrib import messages
from django.contrib.messages.views import SuccessMessageMixin
# from django.contrib.auth.mixins import LoginRequiredMixin,\
#     UserPassesTestMixin
# from django.db.models import ProtectedError
from django.shortcuts import redirect
from django.urls import reverse_lazy
from django.views.generic import ListView
from django.views.generic.edit import CreateView, UpdateView, DeleteView
from django.utils.translation import gettext as _
from task_manager.messages import USER_CREATE_MESSAGE, USER_UPDATE_MESSAGE,\
    USER_DELETE_MESSAGE, PROTECTED_ERROR_MESSAGE
from users.forms import UserRegistrationForm
from users.mixins import UserPermissionMixin
from users.models import User
from tasks.models import Task


class UserListView(ListView):
    model = User
    template_name = 'lists/user.html'


class UserCreateView(SuccessMessageMixin, CreateView):
    form_class = UserRegistrationForm
    model = User
    template_name = 'edit.html'
    extra_context = {'title': _('Registration'),
                     'button_text': _('Register')}
    success_message = USER_CREATE_MESSAGE
    success_url = reverse_lazy('login')


class UserUpdateView(UserPermissionMixin,
                     SuccessMessageMixin, UpdateView):
    model = User
    form_class = UserRegistrationForm
    template_name = 'edit.html'
    extra_context = {'title': _('Update user'),
                     'button_text': _('Update')}
    success_url = reverse_lazy('users:users')
    success_message = USER_UPDATE_MESSAGE
    login_url = reverse_lazy('login')

    # def test_func(self):
    #     user = self.get_object()
    #     return self.request.user.id == user.id
    #
    # def handle_no_permission(self):
    #     if self.request.user.is_authenticated:
    #         messages.warning(self.request, NO_USER_PERMISSION_MESSAGE)
    #         url = reverse_lazy('users:users')
    #     else:
    #         url = self.login_url
    #         messages.warning(self.request, NO_AUTHORIZATION_MESSAGE)
    #     return redirect(url)


class UserDeleteView(UserPermissionMixin,
                     SuccessMessageMixin,
                     DeleteView):
    model = User
    template_name = 'delete.html'
    extra_context = {'title': _('Delete user')}
    success_url = reverse_lazy('users:users')
    login_url = reverse_lazy('login')
    success_message = USER_DELETE_MESSAGE

    # def test_func(self):
    #     user = self.get_object()
    #     return self.request.user.id == user.id
    #
    # def handle_no_permission(self):
    #     if self.request.user.is_authenticated:
    #         messages.warning(self.request, NO_USER_PERMISSION_MESSAGE)
    #         url = reverse_lazy('users:users')
    #     else:
    #         url = self.login_url
    #         messages.warning(self.request, NO_AUTHORIZATION_MESSAGE)
    #     return redirect(url)

    def post(self, request, *args, **kwargs):
        authors_and_executors = Task.objects.values_list('author', 'executor')
        if self.request.user.id in authors_and_executors:
            messages.warning(self.request, PROTECTED_ERROR_MESSAGE)
            return redirect(self.success_url)
        return super().post(request, *args, **kwargs)

    # def form_valid(self, form):
    #     success_url = self.get_success_url()
    #     try:
    #         self.object.delete()
    #         messages.success(self.request, USER_DELETE_MESSAGE)
    #         return redirect(self.success_url)
    #     except ProtectedError:
    #         messages.warning(self.request, PROTECTED_ERROR_MESSAGE)
    #         return redirect(success_url)
