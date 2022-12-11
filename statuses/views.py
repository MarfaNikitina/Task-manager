from django.contrib import messages
from django.contrib.messages.views import SuccessMessageMixin
from django.contrib.auth.mixins import LoginRequiredMixin
from django.db.models import ProtectedError
from django.http import HttpResponseRedirect
from django.shortcuts import redirect
from django.urls import reverse_lazy
from django.views.generic import ListView, CreateView, UpdateView, DeleteView
from statuses.forms import StatusForm
from statuses.models import Status
from django.utils.translation import gettext as _
from task_manager.messages import NO_PERMISSION_MESSAGE,\
    STATUS_CREATE_MESSAGE, STATUS_UPDATE_MESSAGE,\
    STATUS_DELETE_MESSAGE, NO_DELETE_STATUS_MESSAGE


class StatusListView(LoginRequiredMixin, ListView):
    model = Status
    template_name = 'lists/status_list.html'

    def handle_no_permission(self):
        messages.warning(self.request, NO_PERMISSION_MESSAGE)
        return redirect(self.login_url)


class StatusCreateView(LoginRequiredMixin, SuccessMessageMixin, CreateView):
    form_class = StatusForm
    model = Status
    template_name = 'edit.html'
    extra_context = {
        'title': _('Create status'),
        'button_text': _('Create')
    }

    def get_success_url(self):
        messages.success(self.request, STATUS_CREATE_MESSAGE)
        return reverse_lazy('statuses')

    def handle_no_permission(self):
        messages.warning(self.request, NO_PERMISSION_MESSAGE)
        return redirect(self.login_url)


class StatusUpdateView(LoginRequiredMixin, UpdateView):
    model = Status
    form_class = StatusForm
    template_name = 'edit.html'
    extra_context = {
        'title': _('Update status'),
        'button_text': _('Update')
    }

    def get_success_url(self):
        messages.success(self.request, STATUS_UPDATE_MESSAGE)
        return reverse_lazy('statuses')

    def handle_no_permission(self):
        messages.warning(self.request, NO_PERMISSION_MESSAGE)
        return redirect(self.login_url)


class StatusDeleteView(LoginRequiredMixin, DeleteView):
    model = Status
    template_name = 'delete.html'
    extra_context = {
        'title': _('Delete status')
    }
    success_url = reverse_lazy('statuses')

    def handle_no_permission(self):
        messages.warning(self.request, NO_PERMISSION_MESSAGE)
        return redirect(self.login_url)

    def form_valid(self, form):
        success_url = self.get_success_url()
        try:
            self.object.delete()
            messages.success(self.request, STATUS_DELETE_MESSAGE)
        except ProtectedError:
            messages.error(self.request, NO_DELETE_STATUS_MESSAGE)
        finally:
            return HttpResponseRedirect(success_url)
