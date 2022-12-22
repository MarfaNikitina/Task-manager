from django.contrib.auth.forms import UserCreationForm
from .models import User
from django.utils.translation import gettext as _


class UserRegistrationForm(UserCreationForm):

    def __init__(self, *args, **kwargs) -> None:
        super().__init__(*args, **kwargs)
        self.fields['last_name'].required = True
        self.fields['first_name'].requred = True

    class Meta:
        model = User
        fields = ['first_name', 'last_name', 'username']
        labels = dict(username=_('Username'),
                      first_name=_('Name'),
                      last_name=_('Surname'),
                      )
