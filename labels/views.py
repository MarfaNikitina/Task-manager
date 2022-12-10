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

NO_PERMISSION_MESSAGE = _('Вы не авторизованы! Пожалуйста, выполните вход.')
NO_DELETE_MASSAGE = _('Невозможно удалить метку, потому что она используется')


class LabelListView(ListView):
    model = Label
    template_name = 'lists/label_list.html'


class LabelCreateView(LoginRequiredMixin, SuccessMessageMixin, CreateView):
    form_class = LabelForm
    model = Label
    template_name = 'edit.html'
    login_url = 'login'
    extra_context = {'title': _('Создать метку'),
                     'button_text': _('Создать')}

    def get_success_url(self):
        messages.success(self.request, _('Метка успешно создана'))
        return reverse_lazy('labels')

    def handle_no_permission(self):
        messages.warning(self.request, NO_PERMISSION_MESSAGE)
        return redirect(self.login_url)


class LabelUpdateView(LoginRequiredMixin, UpdateView):
    model = Label
    form_class = LabelForm
    template_name = 'edit.html'
    extra_context = {'title': _('Изменение метки'),
                     'button_text': _('Изменить')}

    def get_success_url(self):
        messages.success(self.request, _('Метка успешно изменена'))
        return reverse_lazy('labels')

    def handle_no_permission(self):
        messages.warning(self.request, NO_PERMISSION_MESSAGE)
        return redirect(self.login_url)


class LabelDeleteView(LoginRequiredMixin, DeleteView):
    model = Label
    template_name = 'delete.html'
    extra_context = {'title': _('Удаление метки')}
    success_url = reverse_lazy('labels')

    def handle_no_permission(self):
        messages.warning(self.request, NO_PERMISSION_MESSAGE)
        return redirect(self.login_url)

    def form_valid(self, form):
        success_url = self.get_success_url()
        try:
            self.object.delete()
            messages.success(self.request, _('Метка успешно удалена'))
        except ProtectedError:
            messages.error(self.request, NO_DELETE_MASSAGE)
        finally:
            return HttpResponseRedirect(success_url)
