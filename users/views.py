from django.contrib import messages
from django.shortcuts import render
from django.contrib.messages.views import SuccessMessageMixin
from django.urls import reverse_lazy
from django.contrib.auth.models import User
from django.views.generic import ListView
from django.views.generic.edit import CreateView, UpdateView, DeleteView
from django.utils.translation import gettext as _
from django.contrib.auth.mixins import LoginRequiredMixin

from task_manager.form import UserRegistrationForm


class UserListView(ListView):
    model = User
    template_name = 'users/user_list.html'


class UserCreateView(SuccessMessageMixin, CreateView):
    form_class = UserRegistrationForm
    model = User
    template_name = 'users/user_form.html'

    def get_success_url(self):
        messages.success(self.request, _('Пользователь успешно зарегистрирован'))
        return reverse_lazy('home')


class UserUpdateView(UpdateView):
    model = User
    form_class = UserRegistrationForm
    template_name = 'users/user_update_form.html'

    def get_success_url(self):
        messages.success(self.request, _('Пользователь успешно изменён'))
        return reverse_lazy('users')


class UserDeleteView(DeleteView):
    model = User
    template_name = 'users/user_delete_form.html'

    def get_success_url(self):
        messages.success(self.request, _('Пользователь успешно удален'))
        return reverse_lazy('users')
