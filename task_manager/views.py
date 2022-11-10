from django.views.generic import TemplateView
# from django.utils.translation import gettext as _
from django.contrib.auth.models import User
from django.views.generic import ListView


class IndexView(TemplateView):
    template_name = "index.html"
    
    
class UserListView(ListView):
    model = User