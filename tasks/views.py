from django.contrib import messages
from django.contrib.messages.views import SuccessMessageMixin
from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import render
from django.urls import reverse_lazy
from django.views.generic import ListView, CreateView, UpdateView, DeleteView
from statuses.forms import StatusForm
from statuses.models import Status
from django.utils.translation import gettext as _


class StatusListView(ListView):
    model = Task
    template_name = ''


class StatusCreateView(LoginRequiredMixin, SuccessMessageMixin, CreateView):
    form_class = TaskForm
    model = Task
    template_name = 'statuses/create_status.html'

    def get_success_url(self):
        messages.success(self.request, _('Статус успешно создан'))
        return reverse_lazy('tasks')


class StatusUpdateView(LoginRequiredMixin, UpdateView):
    model = Status
    form_class = StatusForm
    template_name = 'tasks/update_task.html'

    def get_success_url(self):
        messages.success(self.request, _('Статус успешно изменён'))
        return reverse_lazy('tasks')


class StatusDeleteView(LoginRequiredMixin, DeleteView):
    model = Task
    template_name = 'tasks/delete_task.html'

    def get_success_url(self):
        # messages.error(self.request, _('Невозможно удалить статус, потому что он используется'))
        messages.success(self.request, _('Статус успешно удален'))
        return reverse_lazy('tasks')

