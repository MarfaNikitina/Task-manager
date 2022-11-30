# from django.contrib.auth.models import User
from django.contrib.auth.forms import AuthenticationForm, UserCreationForm
from .models import User
from django import forms
from django.utils.translation import gettext as _


class UserRegistrationForm(UserCreationForm):
    # password = forms.CharField(
    #     label='Пароль',
    #     widget=forms.PasswordInput,
    #     help_text="Ваш пароль должен содержать как минимум 3 символа.")
    # password2 = forms.CharField(label='Подтверждение пароля',
    #                             widget=forms.PasswordInput,
    #                             help_text="Для подтверждения введите, пожалуйста, пароль ещё раз.")

    class Meta:
        model = User
        fields = ['first_name', 'last_name', 'username']
        # fields = '__all__'
        labels = dict(username='Имя пользователя',
                      first_name='Имя',
                      last_name='Фамилия',
                      )


# class UserAuthenticationForm(AuthenticationForm):
#     class Meta:
#         model = User
#         fields = ['username', 'password']
#         # fields = '__all__'
#         labels = dict(username=_('Имя пользователя'),
#                       password=_('Пароль'),
#                       )
