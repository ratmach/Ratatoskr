# -*- coding: utf-8 -*-
# Generated by Django 1.11.2 on 2017-07-25 14:26
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('example1', '0003_auto_20170718_0654'),
    ]

    operations = [
        migrations.CreateModel(
            name='Message',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('date', models.DateField(auto_created=True)),
                ('name', models.TextField()),
                ('message', models.TextField()),
            ],
            options={
                'verbose_name': 'Message',
            },
        ),
    ]
