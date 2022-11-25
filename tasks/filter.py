import django_filters
from django import forms
from django_filters import filters
from django_filters.widgets import BooleanWidget

from labels.models import Label
from statuses.models import Status
from tasks.models import Task
from users.models import User
from django.utils.translation import gettext as _


class TaskFilter(django_filters.FilterSet):

    def choose_author(self, queryset, name, value):
        if value:
            author = getattr(self.request, 'user', None)
            queryset = queryset.filter(author=author)
        return queryset

    status = filters.ModelChoiceFilter(queryset=Status.objects.all(),
                                       label=_('Статус'))
    executor = filters.ModelChoiceFilter(queryset=User.objects.all(),
                                         label=_('Исполнитель'))
    label = filters.ModelChoiceFilter(queryset=Label.objects.all(),
                                      label=_('Метка'))
    author = filters.BooleanFilter(
        field_name='author',
        label=_('Только свои задачи'),
        method='choose_author',
        widget=forms.widgets.CheckboxInput(attrs={'class': 'form-check-input is_valid center'})
            )

    class Meta:
        model = Task
        fields = ['status', 'executor', 'label', 'author']

# attrs={'class': 'form-check-input'}
# BooleanWidget