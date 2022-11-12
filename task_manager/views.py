from django.contrib.auth import logout
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth.views import LoginView
from django.shortcuts import redirect
from django.views.generic import TemplateView
from django.urls import reverse_lazy
# from django.utils.translation import gettext as _
from django.contrib.auth.models import User


from task_manager.form import UserRegistrationForm


class IndexView(TemplateView):
    template_name = "index.html"


def logout_view(request):
    logout(request)
    return redirect(('login'))


class LoginUser(LoginView):
    form_class = AuthenticationForm
    template_name = 'registration/login.html'
    success_url = reverse_lazy('')



