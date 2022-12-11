from django.db import models
from users.models import User
from labels.models import Label
from statuses.models import Status


class Task(models.Model):
    name = models.CharField(max_length=100)
    description = models.TextField(null=True)
    status = models.ForeignKey(Status, on_delete=models.PROTECT, null=True)
    author = models.ForeignKey(User, on_delete=models.PROTECT, default=3)
    executor = models.ForeignKey(
        User,
        on_delete=models.PROTECT,
        null=True,
        related_name='executor'
    )
    time_create = models.DateField(auto_now_add=True)
    labels = models.ManyToManyField(
        Label,
        # through='LabelForTask',
        blank=True
    )

    def __str__(self):
        return self.name


# class LabelForTask(models.Model):
#     task = models.ForeignKey(Task, on_delete=models.CASCADE, null=True)
#     label = models.ForeignKey(Label, on_delete=models.PROTECT, null=True)
