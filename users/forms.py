from django.contrib.auth.forms import UserCreationForm
from .models import User
# from django import forms
from django.utils.translation import gettext as _


class UserRegistrationForm(UserCreationForm):

    class Meta:
        model = User
        fields = ['first_name', 'last_name', 'username']
        labels = dict(username=_('Username'),
                      first_name=_('Name'),
                      last_name=_('Surname'),
                      )
