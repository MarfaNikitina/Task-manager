import django_filters
from django_filters import filters
from django_filters.widgets import BooleanWidget

from labels.models import Label
from statuses.models import Status
from tasks.models import Task
from users.models import User
from django.utils.translation import gettext as _


class TaskFilter(django_filters.FilterSet):

    # @property
    # def qs(self):
    #     parent = super().qs
    #     author = getattr(self.request, 'user', None)
    #     return parent.filter(author=author)

    def choose_author(self, queryset, name, value):
        # construct the full lookup expression.
        lookup = '__'.join([name, 'isnull'])
        return queryset.filter(**{lookup: False})

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
        widget=BooleanWidget()
    )

    class Meta:
        model = Task
        fields = ['status', 'executor', 'label', 'author']
