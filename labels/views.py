from django.contrib import messages
from django.contrib.messages.views import SuccessMessageMixin
from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import redirect
from django.urls import reverse_lazy
from django.views.generic import ListView, CreateView, UpdateView, DeleteView
from django.utils.translation import gettext as _
from labels.forms import LabelForm
from labels.models import Label


class LabelListView(ListView):
    model = Label
    # fields = ['id', 'name', 'status',
    #           'author', 'executor', 'time_create']
    template_name = 'labels/labels_list.html'


class LabelCreateView(LoginRequiredMixin, SuccessMessageMixin, CreateView):
    form_class = LabelForm
    model = Label
    template_name = 'labels/create_label.html'
    login_url = 'login'
    extra_context = {'title': _('Создать метку'),
                     'button_text': _('Создать')}

    def get_success_url(self):
        messages.success(self.request, _('Метка успешно создана'))
        return reverse_lazy('labels')

    # def handle_no_permission(self):
    #     messages.warning(self.request, _('Задача успешно создана'))
    #     return redirect(self.login_url)

    def form_valid(self, form):
        self.object = form.save(commit=False)
        self.object.author = self.request.user
        self.object.save()
        return super(LabelCreateView, self).form_valid(form)


class LabelUpdateView(LoginRequiredMixin, UpdateView):
    model = Label
    form_class = LabelForm
    template_name = 'labels/update_label.html'

    def get_success_url(self):
        messages.success(self.request, _('Метка успешно изменена'))
        return reverse_lazy('labels')


class LabelDeleteView(LoginRequiredMixin, DeleteView):
    model = Label
    template_name = 'labels/delete_label.html'

    def get_success_url(self):
        # messages.error(self.request, _('Невозможно удалить статус, потому что он используется'))
        messages.success(self.request, _('Метка успешно удалена'))
        return reverse_lazy('labels')


# class TaskDetail(LoginRequiredMixin, DetailView):
#     template_name = 'tasks/detail_task.html'
#     model = Task

