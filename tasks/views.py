from django.contrib import messages
from django.contrib.messages.views import SuccessMessageMixin
from django.contrib.auth.mixins import LoginRequiredMixin
from django.urls import reverse_lazy
from django.views.generic import ListView, CreateView, UpdateView, DeleteView, DetailView
from statuses.forms import StatusForm
from statuses.models import Status
from django.utils.translation import gettext as _

from tasks.forms import TaskForm
from tasks.models import Task


class TaskListView(ListView):
    model = Task
    template_name = 'tasks/tasks_list.html'


class TaskCreateView(LoginRequiredMixin, SuccessMessageMixin, CreateView):
    form_class = TaskForm
    model = Task
    template_name = 'statuses/create_status.html'

    def get_success_url(self):
        messages.success(self.request, _('Задача успешно создана'))
        return reverse_lazy('tasks')


class TaskUpdateView(LoginRequiredMixin, UpdateView):
    model = Status
    form_class = StatusForm
    template_name = 'tasks/update_task.html'

    def get_success_url(self):
        messages.success(self.request, _('Задача успешно изменена'))
        return reverse_lazy('tasks')


class TaskDeleteView(LoginRequiredMixin, DeleteView):
    model = Task
    template_name = 'tasks/delete_task.html'

    def get_success_url(self):
        # messages.error(self.request, _('Невозможно удалить статус, потому что он используется'))
        messages.success(self.request, _('Задача успешно удалена'))
        return reverse_lazy('tasks')


class TaskDetail(DetailView):
    template_name = 'tasks/detail_task.html'
    model = Task
