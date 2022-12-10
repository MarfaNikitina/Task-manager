from django.contrib import messages
from django.contrib.messages.views import SuccessMessageMixin
from django.contrib.auth.mixins import LoginRequiredMixin,\
    UserPassesTestMixin
from django.db.models import ProtectedError
from django.shortcuts import redirect
from django.urls import reverse_lazy
from django.views.generic import ListView
from django.views.generic.edit import CreateView, UpdateView, DeleteView
from django.utils.translation import gettext as _
from users.forms import UserRegistrationForm
from users.models import User

NO_PERMISSION_MESSAGE = _("У вас нет прав для изменения другого пользователя.")
CREATE_MESSAGE = _('Пользователь успешно зарегистрирован')
NO_LOGIN_MESSAGE = _("Вы не авторизованы! Пожалуйста, выполните вход.")
PROTECTED_ERROR_MESSAGE = _(
    "Нельзя удалить пользователя, так как он используется"
)


class UserListView(ListView):
    model = User
    template_name = 'lists/user_list.html'


class UserCreateView(SuccessMessageMixin, CreateView):
    form_class = UserRegistrationForm
    model = User
    template_name = 'edit.html'
    extra_context = {'title': _('Регистрация'),
                     'button_text': _('Зарегистрировать')}

    def get_success_url(self):
        messages.success(self.request, CREATE_MESSAGE)
        return reverse_lazy('login')


class UserUpdateView(
    LoginRequiredMixin, UserPassesTestMixin,
    SuccessMessageMixin, UpdateView
):
    model = User
    form_class = UserRegistrationForm
    template_name = 'edit.html'
    extra_context = {'title': _('Изменение пользователя'),
                     'button_text': _('Изменить')}
    success_url = reverse_lazy('users:users')
    success_message = _('Пользователь успешно изменён')
    login_url = reverse_lazy('login')

    def test_func(self):
        user = self.get_object()
        return self.request.user.id == user.id

    def handle_no_permission(self):
        if self.request.user.is_authenticated:
            messages.warning(self.request, NO_PERMISSION_MESSAGE)
            url = reverse_lazy('users:users')
        else:
            url = self.login_url
            messages.warning(self.request, NO_LOGIN_MESSAGE)
        return redirect(url)


class UserDeleteView(LoginRequiredMixin,
                     UserPassesTestMixin,
                     SuccessMessageMixin,
                     DeleteView):
    model = User
    template_name = 'delete.html'
    extra_context = {'title': _('Удаление пользователя')}
    success_url = reverse_lazy('users:users')
    login_url = reverse_lazy('login')
    success_message = _('Пользователь успешно удалён')

    def test_func(self):
        user = self.get_object()
        return self.request.user.id == user.id

    def handle_no_permission(self):
        if self.request.user.is_authenticated:
            messages.warning(self.request, NO_PERMISSION_MESSAGE)
            url = reverse_lazy('users:users')
        else:
            url = self.login_url
            messages.warning(self.request, NO_LOGIN_MESSAGE)
        return redirect(url)

    def form_valid(self, form):
        success_url = self.get_success_url()
        try:
            self.object.delete()
            messages.success(self.request, _('Пользователь успешно удалён'))
            return redirect(self.success_url)
        except ProtectedError:
            messages.warning(self.request, PROTECTED_ERROR_MESSAGE)
            return redirect(success_url)

# DATABASE_URL=postgresql:
# //postgres:EP4dS1GGo2To9LPdtbaQ@containers-us-west-59.railway.app:7551/railway
