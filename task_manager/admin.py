from django.contrib import admin
from statuses.models import Status
from tasks.models import Task


admin.site.register(Task)
admin.site.register(Status)
# admin.site.register(Genre)
# admin.site.register(BookInstance)