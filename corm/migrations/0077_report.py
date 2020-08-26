# Generated by Django 3.0.4 on 2020-08-26 13:40

import datetime
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('corm', '0076_auto_20200826_1245'),
    ]

    operations = [
        migrations.CreateModel(
            name='Report',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=256)),
                ('report_type', models.SmallIntegerField(choices=[(0, 'Growth'), (1, 'Impact'), (2, 'Member')])),
                ('generated', models.DateTimeField(default=datetime.datetime.utcnow)),
                ('data', models.TextField(null=True)),
                ('community', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='corm.Community')),
            ],
        ),
    ]
