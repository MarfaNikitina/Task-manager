import django_filters
from django import forms
from django_filters import filters
# from django_filters.widgets import BooleanWidget

from labels.models import Label
from statuses.models import Status
from tasks.models import Task
from users.models import User
from django.utils.translation import gettext as _


class TaskFilter(django_filters.FilterSet):

    def choose_author(self, queryset, name, value):
        if value:
            author = getattr(self.request, 'user', None)
            return queryset.filter(author=author)
        return queryset

    status = filters.ModelChoiceFilter(
        queryset=Status.objects.all(),
        label=_('Статус')
    )
    executor = filters.ModelChoiceFilter(queryset=User.objects.all(),
                                         label=_('Исполнитель'))
    labels = filters.ModelChoiceFilter(queryset=Label.objects.all(),
                                      label=_('Метка'))
    self_author = filters.BooleanFilter(
        field_name='author',
        widget=forms.widgets.CheckboxInput(
            attrs={'class': 'form-check center'}
        ),
        label=_('Только свои задачи'),
        # label_suffix="",
        method='choose_author'
    )

    class Meta:
        model = Task
        fields = ['status', 'executor', 'labels']

# attrs={'class': 'form-check-input'}
# BooleanWidget
