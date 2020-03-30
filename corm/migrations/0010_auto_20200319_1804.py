# Generated by Django 3.0.4 on 2020-03-19 18:04

from django.db import migrations

def set_contact_source(apps, schema_editor):
    Contact = apps.get_model('corm', 'Contact')
    for convo in Contact.objects.all():
        convo.source = convo.channel.source
        convo.save()

class Migration(migrations.Migration):

    dependencies = [
        ('corm', '0009_auto_20200319_1803'),
    ]

    operations = [
        migrations.RunPython(set_contact_source)
    ]