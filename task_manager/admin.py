from django.contrib import admin
from labels.models import Label
from statuses.models import Status
from tasks.models import Task
from users.models import User


admin.site.register(Label)
admin.site.register(Task)
admin.site.register(Status)
admin.site.register(User)
