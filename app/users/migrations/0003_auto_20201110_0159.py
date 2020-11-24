# Generated by Django 3.0.7 on 2020-11-10 01:59

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0002_auto_20201104_0035'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='user',
            name='turma',
        ),
        migrations.AddField(
            model_name='simulacao',
            name='turma',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='users.Turma'),
        ),
        migrations.AddField(
            model_name='turma',
            name='professor',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL),
        ),
        migrations.AddField(
            model_name='turma',
            name='usuarios',
            field=models.ManyToManyField(related_name='usuario_turma', related_query_name='user', to=settings.AUTH_USER_MODEL, verbose_name='Usuários'),
        ),
        migrations.AddField(
            model_name='user',
            name='nome',
            field=models.CharField(max_length=255, null=True, verbose_name='Nome'),
        ),
        migrations.AlterField(
            model_name='user',
            name='matricula',
            field=models.CharField(max_length=7, verbose_name='Matricula'),
        ),
    ]
