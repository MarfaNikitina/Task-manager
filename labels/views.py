from django.contrib import messages
from django.contrib.messages.views import SuccessMessageMixin
from django.contrib.auth.mixins import LoginRequiredMixin
from django.db.models import ProtectedError
from django.http import HttpResponseRedirect
from django.shortcuts import redirect
from django.urls import reverse_lazy
from django.views.generic import ListView, CreateView, UpdateView, DeleteView
from django.utils.translation import gettext as _
from labels.forms import LabelForm
from labels.models import Label
from messages import LABEL_CREATE_MESSAGE, NO_PERMISSION_MESSAGE,\
    LABEL_UPDATE_MESSAGE, LABEL_DELETE_MESSAGE, NO_DELETE_LABEL_MESSAGE


class LabelListView(ListView):
    model = Label
    template_name = 'lists/label_list.html'


class LabelCreateView(LoginRequiredMixin, SuccessMessageMixin, CreateView):
    form_class = LabelForm
    model = Label
    template_name = 'edit.html'
    login_url = 'login'
    extra_context = {'title': _('Create label'),
                     'button_text': _('Create')}

    def get_success_url(self):
        messages.success(self.request, LABEL_CREATE_MESSAGE)
        return reverse_lazy('labels')

    def handle_no_permission(self):
        messages.warning(self.request, NO_PERMISSION_MESSAGE)
        return redirect(self.login_url)


class LabelUpdateView(LoginRequiredMixin, UpdateView):
    model = Label
    form_class = LabelForm
    template_name = 'edit.html'
    extra_context = {'title': _('Update label'),
                     'button_text': _('Update')}

    def get_success_url(self):
        messages.success(self.request, LABEL_UPDATE_MESSAGE)
        return reverse_lazy('labels')

    def handle_no_permission(self):
        messages.warning(self.request, NO_PERMISSION_MESSAGE)
        return redirect(self.login_url)


class LabelDeleteView(LoginRequiredMixin, DeleteView):
    model = Label
    template_name = 'delete.html'
    extra_context = {'title': _('Delete label')}
    success_url = reverse_lazy('labels')

    def handle_no_permission(self):
        messages.warning(self.request, NO_PERMISSION_MESSAGE)
        return redirect(self.login_url)

    def form_valid(self, form):
        success_url = self.get_success_url()
        try:
            self.object.delete()
            messages.success(self.request, LABEL_DELETE_MESSAGE)
        except ProtectedError:
            messages.error(self.request, NO_DELETE_LABEL_MESSAGE)
        finally:
            return HttpResponseRedirect(success_url)
