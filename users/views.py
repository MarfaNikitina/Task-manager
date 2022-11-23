from django.contrib import messages
from django.contrib.messages.views import SuccessMessageMixin
from django.contrib.auth.mixins import LoginRequiredMixin,\
    UserPassesTestMixin
from django.urls import reverse_lazy
# from django.contrib.auth.models import User
from django.views.generic import ListView
from django.views.generic.edit import CreateView, UpdateView, DeleteView
from django.utils.translation import gettext as _
from users.forms import UserRegistrationForm
from users.models import User


class UserListView(ListView):
    model = User
    template_name = 'lists/user_list.html'


class UserCreateView(SuccessMessageMixin, CreateView):
    form_class = UserRegistrationForm
    model = User
    template_name = 'create.html'
    extra_context = {'title': _('Регистрация'),
                     'button_text': _('Зарегистрировать')}

    def get_success_url(self):
        messages.success(self.request, _('Пользователь успешно зарегистрирован'))
        return reverse_lazy('login')


class UserUpdateView(LoginRequiredMixin, UpdateView):
    model = User
    form_class = UserRegistrationForm
    template_name = 'update.html'
    extra_context = {'title': _('Изменение пользователя'),
                     'button_text': _('Изменить')}

    def get_success_url(self):
        messages.success(self.request, _('Пользователь успешно изменён'))
        return reverse_lazy('users')


class UserDeleteView(LoginRequiredMixin, DeleteView):
    model = User
    template_name = 'delete.html'
    extra_context = {'title': _('Удаление пользователя')}
    success_url = reverse_lazy('users')

    def get_success_url(self):
        messages.success(self.request, _('Пользователь успешно удален'))
        return reverse_lazy('users')
