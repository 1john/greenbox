# -*- coding: utf-8 -*-
# Generated by Django 1.11 on 2017-09-23 00:24
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('sites', '0002_alter_domain_unique'),
        ('showcase', '0004_auto_20170918_2307'),
    ]

    operations = [
        migrations.AddField(
            model_name='team',
            name='site',
            field=models.OneToOneField(default=1, on_delete=django.db.models.deletion.CASCADE, to='sites.Site'),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='team',
            name='template_dir',
            field=models.CharField(blank=True, max_length=64),
        ),
    ]
