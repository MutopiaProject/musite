# -*- coding: utf-8 -*-
# Generated by Django 1.10 on 2016-08-22 21:06
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='AssetMap',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('folder', models.CharField(max_length=128)),
                ('name', models.CharField(blank=True, max_length=64)),
                ('has_lys', models.BooleanField(default=False)),
            ],
            options={
                'ordering': ['folder'],
            },
        ),
        migrations.CreateModel(
            name='Collection',
            fields=[
                ('tag', models.CharField(max_length=32, primary_key=True, serialize=False)),
                ('title', models.CharField(max_length=128)),
            ],
        ),
        migrations.CreateModel(
            name='Composer',
            fields=[
                ('composer', models.CharField(max_length=32, primary_key=True, serialize=False)),
                ('description', models.CharField(max_length=48)),
            ],
            options={
                'ordering': ['composer'],
            },
        ),
        migrations.CreateModel(
            name='Contributor',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=128, unique=True)),
                ('email', models.EmailField(blank=True, max_length=254)),
                ('url', models.URLField(blank=True)),
            ],
            options={
                'ordering': ['name'],
            },
        ),
        migrations.CreateModel(
            name='Instrument',
            fields=[
                ('instrument', models.CharField(max_length=32, primary_key=True, serialize=False)),
                ('in_mutopia', models.BooleanField(default=False)),
            ],
            options={
                'ordering': ['instrument'],
            },
        ),
        migrations.CreateModel(
            name='License',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=64)),
                ('url', models.URLField()),
                ('badge', models.CharField(blank=True, max_length=32)),
                ('active', models.BooleanField(default=False)),
            ],
            options={
                'ordering': ['name'],
            },
        ),
        migrations.CreateModel(
            name='LPVersion',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('version', models.CharField(max_length=24, unique=True)),
                ('major', models.IntegerField(blank=True, null=True)),
                ('minor', models.IntegerField(blank=True, null=True)),
                ('edit', models.CharField(blank=True, max_length=8)),
            ],
        ),
        migrations.CreateModel(
            name='Piece',
            fields=[
                ('piece_id', models.IntegerField(primary_key=True, serialize=False)),
                ('title', models.CharField(max_length=128)),
                ('raw_instrument', models.TextField(blank=True)),
                ('opus', models.CharField(blank=True, default='', max_length=64)),
                ('lyricist', models.CharField(blank=True, default='', max_length=128)),
                ('date_composed', models.CharField(blank=True, max_length=32)),
                ('date_published', models.DateField()),
                ('source', models.TextField(blank=True)),
                ('moreinfo', models.TextField(blank=True, default='')),
                ('composer', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='mutopia.Composer')),
                ('instruments', models.ManyToManyField(to='mutopia.Instrument')),
                ('license', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='mutopia.License')),
                ('maintainer', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='mutopia.Contributor')),
            ],
        ),
        migrations.CreateModel(
            name='Style',
            fields=[
                ('style', models.CharField(max_length=32, primary_key=True, serialize=False)),
                ('slug', models.SlugField(max_length=32)),
                ('in_mutopia', models.BooleanField(default=False)),
            ],
            options={
                'ordering': ['style'],
            },
        ),
        migrations.AddField(
            model_name='piece',
            name='style',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='mutopia.Style'),
        ),
        migrations.AddField(
            model_name='piece',
            name='version',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='mutopia.LPVersion'),
        ),
        migrations.AddField(
            model_name='collection',
            name='pieces',
            field=models.ManyToManyField(to='mutopia.Piece'),
        ),
        migrations.AddField(
            model_name='assetmap',
            name='piece',
            field=models.OneToOneField(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='mutopia.Piece'),
        ),
    ]
