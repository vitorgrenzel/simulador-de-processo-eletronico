# Generated by Django 3.0.7 on 2020-11-10 02:21

import django.contrib.auth.models
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('auth', '0011_update_proxy_permissions'),
        ('users', '0003_auto_20201110_0159'),
    ]

    operations = [
        migrations.AlterField(
            model_name='simulacao',
            name='data_fim',
            field=models.DateTimeField(null=True),
        ),
        migrations.DeleteModel(
            name='Papel',
        ),
        migrations.CreateModel(
            name='Papel',
            fields=[
            ],
            options={
                'verbose_name': 'Papel',
                'verbose_name_plural': 'Papeis',
                'proxy': True,
                'indexes': [],
                'constraints': [],
            },
            bases=('auth.group',),
            managers=[
                ('objects', django.contrib.auth.models.GroupManager()),
            ],
        ),
        migrations.AlterField(
            model_name='user',
            name='groups',
            field=models.ManyToManyField(help_text='The profile this user belongs to. A user will get all permissions granted to each of their profiles.', related_name='user_set', related_query_name='user', to='users.Papel', verbose_name='Papeis'),
        ),
    ]
