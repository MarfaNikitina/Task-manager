from django.contrib import messages
from django.contrib.auth import logout
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth.views import LoginView, LogoutView
from django.contrib.messages.views import SuccessMessageMixin
# from django.http import HttpResponse
# from django.shortcuts import redirect
from django.views.generic import TemplateView
from django.urls import reverse_lazy
from django.utils.translation import gettext as _

from users.models import User


class IndexView(TemplateView):
    template_name = "index.html"


# def logout_view(request):
#     logout(request)
#     messages.info(request, _('Вы разлогинены.'))
#     return redirect('home')


class LoginUser(SuccessMessageMixin, LoginView):
    model = User
    form_class = AuthenticationForm
    template_name = 'registration/login.html'
    success_url = reverse_lazy('home')
    success_message = _('Вы залогинены')


class LogoutUser(SuccessMessageMixin, LogoutView):
    success_url = reverse_lazy('home')
    success_message = _('Вы разлогинены.')
