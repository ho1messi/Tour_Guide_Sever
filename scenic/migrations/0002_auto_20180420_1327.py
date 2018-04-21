# Generated by Django 2.0.3 on 2018-04-20 05:27

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('scenic', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='scenicarea',
            name='latitude',
            field=models.FloatField(default=0.0),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='scenicarea',
            name='longitude',
            field=models.FloatField(default=0.0),
            preserve_default=False,
        ),
    ]
