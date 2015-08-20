# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0004_auto_20150817_1509'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='board',
            name='user',
        ),
        migrations.AddField(
            model_name='board',
            name='name',
            field=models.CharField(default='', max_length=666),
            preserve_default=False,
        ),
        migrations.AlterField(
            model_name='division',
            name='name',
            field=models.CharField(unique=True, max_length=42),
        ),
    ]
