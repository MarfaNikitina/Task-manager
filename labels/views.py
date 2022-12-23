from django.contrib import messages
from django.contrib.messages.views import SuccessMessageMixin
from django.db.models import ProtectedError
from django.http import HttpResponseRedirect
from django.urls import reverse_lazy
from django.views.generic import ListView, CreateView, UpdateView, DeleteView
from django.utils.translation import gettext as _
from labels.forms import LabelForm
from labels.models import Label
from task_manager.messages import LABEL_CREATE_MESSAGE, \
    LABEL_UPDATE_MESSAGE, LABEL_DELETE_MESSAGE, NO_DELETE_LABEL_MESSAGE
from users.mixins import MyLoginRequiredMixin


class LabelListView(ListView):
    model = Label
    template_name = 'lists/label.html'


class LabelCreateView(MyLoginRequiredMixin,
                      SuccessMessageMixin, CreateView):
    form_class = LabelForm
    model = Label
    template_name = 'edit.html'
    login_url = 'login'
    extra_context = {'title': _('Create label'),
                     'button_text': _('Create')}
    success_message = LABEL_CREATE_MESSAGE
    success_url = reverse_lazy('labels')


class LabelUpdateView(MyLoginRequiredMixin,
                      SuccessMessageMixin, UpdateView):
    model = Label
    form_class = LabelForm
    template_name = 'edit.html'
    extra_context = {'title': _('Update label'),
                     'button_text': _('Update')}
    success_message = LABEL_UPDATE_MESSAGE
    success_url = reverse_lazy('labels')


class LabelDeleteView(MyLoginRequiredMixin,
                      SuccessMessageMixin, DeleteView):
    model = Label
    template_name = 'delete.html'
    extra_context = {'title': _('Delete label')}
    success_url = reverse_lazy('labels')
    success_message = LABEL_DELETE_MESSAGE

    def form_valid(self, form):
        success_url = self.get_success_url()
        try:
            self.object.delete()
            messages.success(self.request, LABEL_DELETE_MESSAGE)
        except ProtectedError:
            messages.error(self.request, NO_DELETE_LABEL_MESSAGE)
        finally:
            return HttpResponseRedirect(success_url)
