from django.contrib import messages
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth.views import LoginView, LogoutView
from django.contrib.messages.views import SuccessMessageMixin
from django.views.generic import TemplateView
from django.urls import reverse_lazy
from task_manager.messages import SUCCESS_LOGIN_MESSAGE, SUCCESS_LOGOUT_MESSAGE
from users.models import User


class IndexView(TemplateView):
    template_name = "index.html"


class LoginUser(SuccessMessageMixin, LoginView):
    model = User
    form_class = AuthenticationForm
    template_name = 'registration/login.html'
    success_url = reverse_lazy('home')
    success_message = SUCCESS_LOGIN_MESSAGE


class LogoutUser(SuccessMessageMixin, LogoutView):

    def get_success_url(self):
        messages.success(self.request, SUCCESS_LOGOUT_MESSAGE)
        return reverse_lazy('home')
