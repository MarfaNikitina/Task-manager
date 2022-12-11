from django import forms
from .models import Label
from django.utils.translation import gettext as _


class LabelForm(forms.ModelForm):
    class Meta:
        model = Label
        fields = ['name']
        labels = {
            'name': _('Name'),
        }
