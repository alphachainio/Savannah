# Generated by Django 3.0.4 on 2020-03-04 22:11

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('corm', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='community',
            name='name',
            field=models.CharField(default='null', max_length=256),
            preserve_default=False,
        ),
    ]