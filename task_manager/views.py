from django.contrib import messages
from django.contrib.auth import logout
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth.views import LoginView
from django.contrib.messages.views import SuccessMessageMixin
from django.http import HttpResponse
from django.shortcuts import redirect
from django.views.generic import TemplateView
from django.urls import reverse_lazy
from django.utils.translation import gettext as _

from users.models import User


def index(request):
    a = None
    a.hello()
    return HttpResponse("Hello, world. You're at the pollapp index.")


class IndexView(TemplateView):
    template_name = "index.html"


def logout_view(request):
    logout(request)
    messages.info(request, _('Вы разлогинены.'))
    return redirect('home')


class LoginUser(SuccessMessageMixin, LoginView):
    model = User
    form_class = AuthenticationForm
    template_name = 'registration/login.html'
    success_url = reverse_lazy('home')
    success_message = _('Вы залогинены')

    # def get_success_url(self):
    #     messages.info(self.request, _('Вы залогинены'))
    #     return reverse_lazy('home')

# DATABASE_URL=postgresql://postgres:EP4dS1GGo2To9LPdtbaQ@$containers-us-west-152.railway.app:5919/railway