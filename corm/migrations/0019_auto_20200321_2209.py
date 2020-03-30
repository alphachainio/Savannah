# Generated by Django 3.0.4 on 2020-03-21 22:09

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('corm', '0018_auto_20200321_2051'),
    ]

    operations = [
        migrations.AddField(
            model_name='source',
            name='auth_id',
            field=models.CharField(blank=True, max_length=256, null=True),
        ),
        migrations.AddField(
            model_name='source',
            name='auth_secret',
            field=models.CharField(blank=True, max_length=256, null=True),
        ),
        migrations.AlterField(
            model_name='activity',
            name='tags',
            field=models.ManyToManyField(blank=True, to='corm.Tag'),
        ),
        migrations.AlterField(
            model_name='conversation',
            name='tags',
            field=models.ManyToManyField(blank=True, to='corm.Tag'),
        ),
        migrations.AlterField(
            model_name='member',
            name='tags',
            field=models.ManyToManyField(blank=True, to='corm.Tag'),
        ),
        migrations.AlterField(
            model_name='note',
            name='tags',
            field=models.ManyToManyField(blank=True, to='corm.Tag'),
        ),
        migrations.AlterField(
            model_name='project',
            name='tags',
            field=models.ManyToManyField(blank=True, to='corm.Tag'),
        ),
        migrations.AlterField(
            model_name='source',
            name='connector',
            field=models.CharField(choices=[('corm.plugins.null', 'Manual Entry'), ('corm.plugins.email', 'Email'), ('corm.plugins.slack', 'Slack'), ('corm.plugins.discourse', 'Discourse'), ('corm.plugins.rss', 'RSS'), ('corm.plugins.reddit', 'Reddit'), ('corm.plugins.github', 'Github')], max_length=256),
        ),
        migrations.AlterField(
            model_name='source',
            name='server',
            field=models.CharField(blank=True, max_length=256, null=True),
        ),
        migrations.AlterField(
            model_name='task',
            name='tags',
            field=models.ManyToManyField(blank=True, to='corm.Tag'),
        ),
    ]