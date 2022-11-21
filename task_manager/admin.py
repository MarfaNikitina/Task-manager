from django.contrib import admin
from labels.models import Label
from statuses.models import Status
from tasks.models import Task


admin.site.register(Label)
admin.site.register(Task)
admin.site.register(Status)
