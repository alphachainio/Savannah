# Generated by Django 3.0.4 on 2020-03-24 13:10

from django.db import migrations

def set_task_community(apps, schema_editor):
    Task = apps.get_model('corm', 'Task')
    for task in Task.objects.all():
        task.community = task.project.community
        task.save()


class Migration(migrations.Migration):

    dependencies = [
        ('corm', '0020_auto_20200324_1310'),
    ]

    operations = [
        migrations.RunPython(set_task_community)
    ]
