from django.contrib import messages
from django.contrib.messages.views import SuccessMessageMixin
from django.contrib.auth.mixins import UserPassesTestMixin
from django.db.models import ProtectedError
from django.shortcuts import redirect
from django.urls import reverse_lazy
from django.views.generic import CreateView, UpdateView, DeleteView, DetailView
from django.utils.translation import gettext as _
from django_filters.views import FilterView
from task_manager.messages import TASK_CREATE_MESSAGE, \
    TASK_UPDATE_MESSAGE, NO_DELETE_TASK_MESSAGE, TASK_DELETE_MESSAGE
from tasks.filter import TaskFilter
from tasks.forms import TaskForm
from tasks.models import Task
from users.mixins import MyLoginRequiredMixin


class TaskListView(FilterView):
    model = Task
    fields = ['id', 'name', 'status',
              'author', 'executor', 'time_create']
    template_name = 'lists/task.html'
    filterset_class = TaskFilter


class TaskCreateView(MyLoginRequiredMixin,
                     SuccessMessageMixin,
                     CreateView):
    form_class = TaskForm
    model = Task
    template_name = 'edit.html'
    login_url = 'login'
    extra_context = {'title': _('Create task'),
                     'button_text': _('Create')}
    success_message = TASK_CREATE_MESSAGE
    success_url = reverse_lazy('tasks')

    def form_valid(self, form):
        form.instance.author = self.request.user
        return super().form_valid(form)


class TaskUpdateView(MyLoginRequiredMixin,
                     SuccessMessageMixin,
                     UpdateView):
    model = Task
    form_class = TaskForm
    login_url = 'login'
    template_name = 'edit.html'
    extra_context = {'title': _('Update task'),
                     'button_text': _('Update')}
    success_message = TASK_UPDATE_MESSAGE
    success_url = reverse_lazy('tasks')


class TaskDeleteView(MyLoginRequiredMixin,
                     UserPassesTestMixin,
                     SuccessMessageMixin,
                     DeleteView):
    model = Task
    login_url = 'login'
    template_name = 'tasks/delete_task.html'
    success_url = reverse_lazy('tasks')
    success_message = TASK_DELETE_MESSAGE

    def test_func(self):
        return self.get_object().author == self.request.user

    def handle_no_permission(self):
        url = reverse_lazy('tasks')
        messages.warning(self.request, NO_DELETE_TASK_MESSAGE)
        return redirect(url)

    def form_valid(self, form):
        try:
            self.object.delete()
            messages.success(self.request, TASK_DELETE_MESSAGE)
            return redirect(self.success_url)
        except ProtectedError:
            messages.warning(self.request,
                             NO_DELETE_TASK_MESSAGE)
            return redirect(self.success_url)


class TaskDetail(MyLoginRequiredMixin, DetailView):
    template_name = 'tasks/detail_task.html'
    model = Task
