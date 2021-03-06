# -*- coding: utf-8 -*-
# Generated by Django 1.11.3 on 2017-10-03 16:54
from __future__ import unicode_literals

from django.db import migrations, models
import fms.models


class Migration(migrations.Migration):

    dependencies = [
        ('fms', '0015_gallery_info'),
    ]

    operations = [
        migrations.RenameField(
            model_name='donate_info',
            old_name='latitude',
            new_name='city',
        ),
        migrations.RenameField(
            model_name='donate_info',
            old_name='longitude',
            new_name='locality',
        ),
        migrations.AddField(
            model_name='donate_info',
            name='mobile',
            field=models.IntegerField(null=True),
        ),
        migrations.AddField(
            model_name='donate_info',
            name='street',
            field=models.CharField(max_length=100, null=True),
        ),
        migrations.AlterField(
            model_name='gallery_info',
            name='image',
            field=models.FileField(upload_to=fms.models.get_gallery_file_name),
        ),
    ]
