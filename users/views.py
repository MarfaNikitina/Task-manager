from django.contrib import messages
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth.views import LoginView
from django.contrib.messages.views import SuccessMessageMixin
from django.contrib.auth.mixins import LoginRequiredMixin,\
    UserPassesTestMixin
from django.db.models import ProtectedError
from django.shortcuts import redirect, render
from django.urls import reverse_lazy
from django.views.generic import ListView
from django.views.generic.edit import CreateView, UpdateView, DeleteView
from django.utils.translation import gettext as _
from users.forms import UserRegistrationForm
from users.models import User
from django.contrib.auth import authenticate, login, logout


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


class UserUpdateView(LoginRequiredMixin, UserPassesTestMixin, SuccessMessageMixin, UpdateView):
    model = User
    form_class = UserRegistrationForm
    template_name = 'update.html'
    extra_context = {'title': _('Изменение пользователя'),
                     'button_text': _('Изменить')}
    success_url = reverse_lazy('users:users')
    success_message = _('Пользователь успешно изменён')
    login_url = reverse_lazy('login')

    def test_func(self):
        user = self.get_object()
        return self.request.user.id == user.id

    def handle_no_permission(self):
        # if self.request.user.is_authenticated:
        message =_("У вас нет прав для изменения другого пользователя.")
        url = reverse_lazy('users:users')
        # else:
        #     message = _("Вы не авторизованы! Пожалуйста, выполните вход.")
        #     url = self.login_url
        messages.warning(self.request, message)
        return redirect(url)

    # def form_valid(self, form):
    #     form.save()
    #     username = self.request.POST['username']
    #     password = self.request.POST['password']
    #     user = authenticate(username=username, password=password)
    #     login(self.request, user)
    #     messages.success(self.request, _('Пользователь успешно изменён'))
    #     return redirect(self.success_url)


class UserDeleteView(LoginRequiredMixin, UserPassesTestMixin, DeleteView):
    model = User
    template_name = 'delete.html'
    extra_context = {'title': _('Удаление пользователя')}
    success_url = reverse_lazy('users:users')

    def test_func(self):
        user = self.get_object()
        return self.request.user.id == user.id

    def handle_no_permission(self):
        message = _("У вас нет прав для изменения другого пользователя.")
        messages.warning(self.request, message)
        return redirect(reverse_lazy('users:users'))

    def form_valid(self, form):
        success_url = self.get_success_url()
        try:
            self.object.delete()
            messages.success(self.request, _('Пользователь успешно удалён'))
            return redirect(self.success_url)
        except ProtectedError:
            messages.warning(self.request,
                             _("У вас нет прав для изменения другого пользователя."))
            return redirect(success_url)
