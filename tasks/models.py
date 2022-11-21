from django.db import models
from django.contrib.auth.models import User

from labels.models import Label
from statuses.models import Status


class Task(models.Model):
    name = models.CharField(max_length=100)
    description = models.TextField(null=True)
    status = models.ForeignKey(Status, on_delete=models.PROTECT, null=True)
    author = models.ForeignKey(User, on_delete=models.PROTECT)
    executor = models.ForeignKey(User, on_delete=models.PROTECT, null=True, related_name='executor')
    time_create = models.DateField(auto_now_add=True)
    labels = models.ManyToManyField(Label)

    def __str__(self):
        return self.name
