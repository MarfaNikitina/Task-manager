# Generated by Django 4.1.2 on 2022-12-11 16:42

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('labels', '0001_initial'),
        ('tasks', '0003_rename_label_task_labels'),
    ]

    operations = [
        migrations.AlterField(
            model_name='task',
            name='labels',
            field=models.ManyToManyField(blank=True, to='labels.label'),
        ),
        migrations.DeleteModel(
            name='LabelForTask',
        ),
    ]
