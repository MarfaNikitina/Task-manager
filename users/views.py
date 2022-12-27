from django.contrib import messages
from django.contrib.messages.views import SuccessMessageMixin
from django.shortcuts import redirect
from django.urls import reverse_lazy
from django.views.generic import ListView
from django.views.generic.edit import CreateView, UpdateView, DeleteView
from django.utils.translation import gettext as _
from task_manager.messages import USER_CREATE_MESSAGE, USER_UPDATE_MESSAGE,\
    USER_DELETE_MESSAGE, PROTECTED_ERROR_MESSAGE
from users.forms import UserRegistrationForm
from task_manager.mixins import UserPermissionMixin, MyLoginRequiredMixin
from users.models import User
from tasks.models import Task
from django.db.models import Q


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


class UserUpdateView(UserPermissionMixin, MyLoginRequiredMixin,
                     SuccessMessageMixin, UpdateView):
    model = User
    form_class = UserRegistrationForm
    template_name = 'edit.html'
    extra_context = {'title': _('Update user'),
                     'button_text': _('Update')}
    success_message = USER_UPDATE_MESSAGE
    success_url = reverse_lazy('users:users')
    login_url = reverse_lazy('login')


class UserDeleteView(UserPermissionMixin,
                     MyLoginRequiredMixin,
                     SuccessMessageMixin,
                     DeleteView):
    model = User
    template_name = 'delete.html'
    extra_context = {'title': _('Delete user')}
    success_url = reverse_lazy('users:users')
    login_url = reverse_lazy('login')
    success_message = USER_DELETE_MESSAGE

    def post(self, request, *args, **kwargs):
        if Task.objects.filter(
                Q(executor_id=self.kwargs['pk']) | Q(author_id=self.kwargs['pk'])):
            messages.warning(self.request, PROTECTED_ERROR_MESSAGE)
            return redirect(self.success_url)
        return super().post(request, *args, **kwargs)
