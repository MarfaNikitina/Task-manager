from django.contrib.auth.forms import UserCreationForm, UserChangeForm
from .models import User
# from django import forms
from django.utils.translation import gettext as _


class UserRegistrationForm(UserCreationForm):

    class Meta:
        model = User
        fields = ['first_name', 'last_name', 'username']
        labels = dict(username=_('Имя пользователя'),
                      first_name=_('Имя'),
                      last_name=_('Фамилия'),
                      )
