# from django.contrib.auth.models import User
from .models import User
from django import forms
from django.utils.translation import gettext as _


class UserRegistrationForm(forms.ModelForm):
    password = forms.CharField(
        label='Пароль',
        widget=forms.PasswordInput,
        help_text="Ваш пароль должен содержать как минимум 3 символа.")
    password2 = forms.CharField(label='Подтверждение пароля',
                                widget=forms.PasswordInput,
                                help_text="Для подтверждения введите, пожалуйста, пароль ещё раз.")

    class Meta:
        model = User
        fields = ['first_name', 'last_name', 'username']
        # fields = '__all__'
        labels = dict(username='Имя пользователя',
                      first_name='Имя',
                      last_name='Фамилия',
                      )

    def clean_password2(self):
        cd = self.cleaned_data
        if cd['password'] != cd['password2']:
            raise forms.ValidationError(_('Введённые пароли не совпадают.'))
        return cd['password2']
