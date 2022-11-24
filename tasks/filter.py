import django_filters
from django_filters import filters

from labels.models import Label
from statuses.models import Status
from tasks.models import Task
from users.models import User


class TaskFilter(django_filters.FilterSet):

    @property
    def qs(self):
        parent = super().qs
        author = getattr(self.request, 'user', None)

        return parent.filter(author=author)

    status = filters.ModelChoiceFilter(queryset=Status.objects.all(),
                                       )
    executor = filters.ModelChoiceFilter(queryset=User.objects.all())
    label = filters.ModelChoiceFilter(queryset=Label.objects.all())

    class Meta:
        model = Task
        fields = ['status', 'executor', 'label']


