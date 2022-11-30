from django.contrib import messages
from django.contrib.auth import logout
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth.views import LoginView, LogoutView
from django.contrib.messages.views import SuccessMessageMixin
from django.shortcuts import redirect
from django.views.generic import TemplateView
from django.urls import reverse_lazy
from django.utils.translation import gettext as _


class IndexView(TemplateView):
    template_name = "index.html"


def logout_view(request):
    logout(request)
    messages.info(request, _('Вы разлогинены.'))
    return redirect('home')


class LoginUser(LoginView):
    form_class = AuthenticationForm
    template_name = 'registration/login.html'

    def get_success_url(self):
        messages.info(self.request, _('Вы залогинены'))
        return reverse_lazy('home')


# class LoginUser(SuccessMessageMixin, LoginView):
#     form_class = AuthenticationForm
#     template_name = 'registration/login.html'
#     success_message = _('Вы залогинены')




