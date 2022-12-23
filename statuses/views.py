from django.contrib import messages
from django.contrib.messages.views import SuccessMessageMixin
from django.db.models import ProtectedError
from django.http import HttpResponseRedirect
from django.urls import reverse_lazy
from django.views.generic import ListView, CreateView, UpdateView, DeleteView
from statuses.forms import StatusForm
from statuses.models import Status
from django.utils.translation import gettext as _
from task_manager.messages import STATUS_CREATE_MESSAGE,\
    STATUS_UPDATE_MESSAGE,\
    STATUS_DELETE_MESSAGE, NO_DELETE_STATUS_MESSAGE
from users.mixins import MyLoginRequiredMixin


class StatusListView(MyLoginRequiredMixin, ListView):
    model = Status
    template_name = 'lists/status.html'


class StatusCreateView(MyLoginRequiredMixin,
                       SuccessMessageMixin, CreateView):
    form_class = StatusForm
    model = Status
    template_name = 'edit.html'
    extra_context = {
        'title': _('Create status'),
        'button_text': _('Create')
    }
    success_message = STATUS_CREATE_MESSAGE
    success_url = reverse_lazy('statuses')


class StatusUpdateView(MyLoginRequiredMixin,
                       SuccessMessageMixin,
                       UpdateView):
    model = Status
    form_class = StatusForm
    template_name = 'edit.html'
    extra_context = {
        'title': _('Update status'),
        'button_text': _('Update')
    }
    success_message = STATUS_UPDATE_MESSAGE
    success_url = reverse_lazy('statuses')


class StatusDeleteView(MyLoginRequiredMixin,
                       SuccessMessageMixin,
                       DeleteView):
    model = Status
    template_name = 'delete.html'
    extra_context = {
        'title': _('Delete status')
    }
    success_url = reverse_lazy('statuses')
    success_message = STATUS_DELETE_MESSAGE

    def form_valid(self, form):
        success_url = self.get_success_url()
        try:
            self.object.delete()
            messages.success(self.request, STATUS_DELETE_MESSAGE)
        except ProtectedError:
            messages.error(self.request, NO_DELETE_STATUS_MESSAGE)
        finally:
            return HttpResponseRedirect(success_url)
