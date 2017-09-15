# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Sections',
            fields=[
                ('id', models.AutoField(primary_key=True, auto_created=True, serialize=False, verbose_name='ID')),
                ('section_name', models.CharField(max_length=30)),
            ],
        ),
        migrations.CreateModel(
            name='Subsection',
            fields=[
                ('id', models.AutoField(primary_key=True, auto_created=True, serialize=False, verbose_name='ID')),
                ('subsection_name', models.CharField(max_length=50)),
                ('section_name', models.ForeignKey(default='other', to='topics.Sections')),
            ],
        ),
        migrations.CreateModel(
            name='TopicAnswers',
            fields=[
                ('id', models.AutoField(primary_key=True, auto_created=True, serialize=False, verbose_name='ID')),
                ('user_name', models.CharField(max_length=100)),
                ('date', models.DateField()),
                ('context', models.TextField()),
            ],
        ),
        migrations.CreateModel(
            name='Topics',
            fields=[
                ('id', models.AutoField(primary_key=True, auto_created=True, serialize=False, verbose_name='ID')),
                ('topic_name', models.CharField(max_length=300)),
                ('date', models.DateField()),
                ('author_name', models.CharField(max_length=100)),
                ('context', models.TextField()),
                ('section_name', models.ForeignKey(default='other', to='topics.Sections')),
                ('subsection_name', models.ForeignKey(default='other', to='topics.Subsection')),
            ],
        ),
        migrations.AddField(
            model_name='topicanswers',
            name='topic_name',
            field=models.ForeignKey(to='topics.Topics'),
        ),
    ]
