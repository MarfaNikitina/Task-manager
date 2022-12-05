from django.contrib import messages
from django.contrib.messages.views import SuccessMessageMixin
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.db.models import ProtectedError
from django.shortcuts import redirect
from django.urls import reverse_lazy
from django.views.generic import CreateView, UpdateView, DeleteView, DetailView
from django.utils.translation import gettext as _
from django_filters.views import FilterView
from tasks.filter import TaskFilter
from tasks.forms import TaskForm
from tasks.models import Task

NO_PERMISSION_MESSAGE = _("Вы не авторизованы! Пожалуйста, выполните вход.")


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

    def handle_no_permission(self):
        messages.warning(self.request, NO_PERMISSION_MESSAGE)
        return redirect(reverse_lazy('login'))

    def form_valid(self, form):
        self.object = form.save(commit=False)
        self.object.author = self.request.user
        self.object.save()
        return super(TaskCreateView, self).form_valid(form)


class TaskUpdateView(LoginRequiredMixin, UpdateView):
    model = Task
    form_class = TaskForm
    login_url = 'login'
    template_name = 'tasks/update_task.html'

    def get_success_url(self):
        messages.success(self.request, _('Задача успешно изменена'))
        return reverse_lazy('tasks')

    def handle_no_permission(self):
        messages.warning(self.request, NO_PERMISSION_MESSAGE)
        return redirect(self.login_url)


class TaskDeleteView(LoginRequiredMixin, UserPassesTestMixin, DeleteView):
    model = Task
    login_url = 'login'
    template_name = 'tasks/delete_task.html'
    success_url = reverse_lazy('tasks')

    def test_func(self):
        return self.get_object().author == self.request.user

    def handle_no_permission(self):
        if self.request.user.is_authenticated:
            message = _("Задачу может удалить только её автор")
            url = reverse_lazy('tasks')
        else:
            message = NO_PERMISSION_MESSAGE
            url = self.login_url
        messages.warning(self.request, message)
        return redirect(url)

    def form_valid(self, form):
        try:
            self.object.delete()
            messages.success(self.request, _('Задача успешно удалена'))
            return redirect(self.success_url)
        except ProtectedError:
            messages.warning(self.request,
                             _("Задачу может удалить только её автор"))
            return redirect(self.success_url)


class TaskDetail(LoginRequiredMixin, DetailView):
    template_name = 'tasks/detail_task.html'
    model = Task

    def handle_no_permission(self):
        messages.warning(self.request, NO_PERMISSION_MESSAGE)
        return redirect(self.login_url)
