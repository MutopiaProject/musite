# -*- coding: utf-8 -*-
# Generated by Django 1.10 on 2016-11-24 18:00
from __future__ import unicode_literals

from django.db import migrations, models, transaction

# We want the default to be False but all existing AssetMap objects
# should be set to True (published) at the time of migration.
def _set_all_published(apps, schema_editor):
    AssetMap = apps.get_model('mutopia', 'AssetMap')
    with transaction.atomic():
        for asset in AssetMap.objects.all():
            asset.published = True;
            asset.save()

class Migration(migrations.Migration):

    dependencies = [
        ('mutopia', '0003_auto_20160905_2257'),
    ]

    operations = [
        migrations.AddField(
            model_name='assetmap',
            name='published',
            field=models.BooleanField(default=False),
        ),
        migrations.RunPython(_set_all_published),
    ]
