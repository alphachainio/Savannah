# Generated by Django 3.0.4 on 2020-03-26 14:20

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('corm', '0027_auto_20200325_1549'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='member',
            name='origin_id',
        ),
    ]
