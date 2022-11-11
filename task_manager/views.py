from django.views.generic import TemplateView
from django.urls import reverse_lazy
# from django.utils.translation import gettext as _
from django.contrib.auth.models import User
from django.views.generic import ListView
from django.views.generic.edit import CreateView, UpdateView, DeleteView

from task_manager.form import UserRegistrationForm


class IndexView(TemplateView):
    template_name = "index.html"


class UserListView(ListView):
    model = User
    template_name = 'user_list.html'


class UserCreateView(CreateView):
    form_class = UserRegistrationForm
    model = User
    template_name = 'user_form.html'
    success_url = '/login'


class UserUpdateView(UpdateView):
    model = User
    form_class = UserRegistrationForm
    template_name = 'user_update_form.html'
    success_url = 'users/'


class UserDeleteView(DeleteView):
    model = User
    success_url = reverse_lazy('users')
    template_name = 'user_delete_form.html'

