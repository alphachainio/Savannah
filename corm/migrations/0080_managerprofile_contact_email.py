# Generated by Django 3.0.4 on 2020-09-05 18:16

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('corm', '0079_auto_20200905_1542'),
    ]

    operations = [
        migrations.AddField(
            model_name='managerprofile',
            name='contact_email',
            field=models.EmailField(blank=True, max_length=254, null=True),
        ),
    ]
