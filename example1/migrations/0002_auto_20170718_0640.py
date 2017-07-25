# -*- coding: utf-8 -*-
# Generated by Django 1.11.2 on 2017-07-18 13:40
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('Ratatoskr', '__first__'),
        ('example1', '0001_initial'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='dataclass',
            name='id',
        ),
        migrations.AddField(
            model_name='dataclass',
            name='abstractnut_ptr',
            field=models.OneToOneField(auto_created=True, default=1, on_delete=django.db.models.deletion.CASCADE, parent_link=True, primary_key=True, serialize=False, to='Ratatoskr.AbstractNut'),
            preserve_default=False,
        ),
        migrations.AlterField(
            model_name='dataclass',
            name='name',
            field=models.CharField(default='abcd', max_length=255),
        ),
    ]