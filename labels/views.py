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


class LabelListView(ListView):
    model = Label
    template_name = 'lists/label_list.html'


class LabelCreateView(LoginRequiredMixin, SuccessMessageMixin, CreateView):
    form_class = LabelForm
    model = Label
    template_name = 'create.html'
    login_url = 'login'
    extra_context = {'title': _('Создать метку'),
                     'button_text': _('Создать')}

    def get_success_url(self):
        messages.success(self.request, _('Метка успешно создана'))
        return reverse_lazy('labels')

    def handle_no_permission(self):
        messages.warning(self.request, _('Вы не авторизованы! Пожалуйста, выполните вход.'))
        return redirect(self.login_url)

    # def form_valid(self, form):
    #     self.object = form.save(commit=False)
    #     self.object.author = self.request.user
    #     self.object.save()
    #     return super(LabelCreateView, self).form_valid(form)


class LabelUpdateView(LoginRequiredMixin, UpdateView):
    model = Label
    form_class = LabelForm
    template_name = 'update.html'
    extra_context = {'title': _('Изменение метки'),
                     'button_text': _('Изменить')}

    def get_success_url(self):
        messages.success(self.request, _('Метка успешно изменена'))
        return reverse_lazy('labels')

    def handle_no_permission(self):
        messages.warning(self.request, _("Вы не авторизованы! Пожалуйста, выполните вход."))
        return redirect(self.login_url)


class LabelDeleteView(LoginRequiredMixin, DeleteView):
    model = Label
    template_name = 'delete.html'
    extra_context = {'title': _('Удаление метки')}
    success_url = reverse_lazy('labels')

    def handle_no_permission(self):
        messages.warning(self.request, _("Вы не авторизованы! Пожалуйста, выполните вход."))
        return redirect(self.login_url)

    def form_valid(self, form):
        success_url = self.get_success_url()
        try:
            self.object.delete()
            messages.success(self.request, _('Метка успешно удалена'))
        except ProtectedError:
            messages.error(self.request, _('Невозможно удалить метку, потому что она используется'))
        finally:
            return HttpResponseRedirect(success_url)
