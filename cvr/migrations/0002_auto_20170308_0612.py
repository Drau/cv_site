# -*- coding: utf-8 -*-
# Generated by Django 1.10.6 on 2017-03-08 06:12
from __future__ import unicode_literals

import cvr.models
from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('cvr', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Profile',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('first_name', models.CharField(max_length=30)),
                ('last_name', models.CharField(max_length=30)),
                ('cv', models.FileField(upload_to=cvr.models.user_directory_path)),
                ('free_text', models.CharField(max_length=200)),
                ('user', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.RemoveField(
            model_name='person',
            name='user',
        ),
        migrations.DeleteModel(
            name='Person',
        ),
    ]
