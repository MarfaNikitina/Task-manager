from django import forms
from django.utils.translation import gettext as _
from labels.models import Label
from .models import Task


class TaskForm(forms.ModelForm):
    class Meta:
        model = Task
        fields = ['name', 'description', 'status', 'executor', 'label']
        # fields = '__all__'
        labels = {
            'name': _('Имя'),
            'description': _('Описание'),
            'status': _('Статус'),
            'executor': _('Исполнитель'),
            'labels': _('Метки')
        }
        # 
        # label = forms.ModelChoiceField(
        #     queryset=Label.objects.all())
