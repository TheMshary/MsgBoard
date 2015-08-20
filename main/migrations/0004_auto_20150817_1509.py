# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0003_remove_division_user'),
    ]

    operations = [
        migrations.AlterField(
            model_name='division',
            name='name',
            field=models.CharField(default='', max_length=42),
            preserve_default=False,
        ),
    ]
