# Generated by Django 2.0.3 on 2018-05-29 02:50

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('scenic', '0004_scenicarea_about'),
    ]

    operations = [
        migrations.AddField(
            model_name='scenicspot',
            name='latitude',
            field=models.FloatField(default=0.0),
        ),
        migrations.AddField(
            model_name='scenicspot',
            name='longitude',
            field=models.FloatField(default=0.0),
        ),
    ]
