from django.contrib import messages
from django.contrib.messages.views import SuccessMessageMixin
from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import render, redirect
from django.urls import reverse_lazy
from django.views.generic import ListView, CreateView, UpdateView, DeleteView, DetailView
from django.utils.translation import gettext as _
from django_filters.views import FilterView
from tasks.filter import TaskFilter
from tasks.forms import TaskForm
from tasks.models import Task


class TaskListView(FilterView):
    model = Task
    fields = ['id', 'name', 'status',
              'author', 'executor', 'time_create']
    template_name = 'lists/task_list.html'
    filterset_class = TaskFilter


class TaskCreateView(LoginRequiredMixin, SuccessMessageMixin, CreateView):
    form_class = TaskForm
    model = Task
    template_name = 'tasks/create_task.html'
    login_url = 'login'
    extra_context = {'title': 'Создать задачу',
                     'button_text': 'Создать'}

    def get_success_url(self):
        messages.success(self.request, _('Задача успешно создана'))
        return reverse_lazy('tasks')

    # def handle_no_permission(self):
    #     # messages.warning(self.request, _('У вас нет прав'))
    #     return redirect(self.login_url)

    def form_valid(self, form):
        self.object = form.save(commit=False)
        self.object.author = self.request.user
        self.object.save()
        return super(TaskCreateView, self).form_valid(form)


class TaskUpdateView(LoginRequiredMixin, UpdateView):
    model = Task
    form_class = TaskForm
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


class TaskDetail(LoginRequiredMixin, DetailView):
    template_name = 'tasks/detail_task.html'
    model = Task
