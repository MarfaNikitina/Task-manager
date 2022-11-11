from django.views.generic import TemplateView
# from django.utils.translation import gettext as _
from django.contrib.auth.models import User
from django.views.generic import ListView
from django.views.generic.edit import CreateView

from task_manager.form import UserRegistrationForm


class IndexView(TemplateView):
    template_name = "index.html"


class UserListView(ListView):
    model = User
    template_name = 'user_list.html'


# class DataMixin:
#     pass


class UserCreateView(CreateView):
    form_class = UserRegistrationForm
    model = User
    template_name = 'user_form.html'
    success_url = '/login'

