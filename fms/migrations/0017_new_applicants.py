# -*- coding: utf-8 -*-
# Generated by Django 1.11.3 on 2017-10-04 00:36
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('fms', '0016_auto_20171003_2224'),
    ]

    operations = [
        migrations.CreateModel(
            name='new_applicants',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=100)),
                ('street', models.CharField(max_length=100)),
                ('locality', models.CharField(max_length=100)),
                ('city', models.CharField(max_length=100)),
                ('mobile', models.IntegerField()),
                ('email', models.EmailField(max_length=254)),
                ('is_a_member', models.BooleanField()),
            ],
        ),
    ]