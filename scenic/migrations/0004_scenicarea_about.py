# Generated by Django 2.0.3 on 2018-05-12 03:16

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('scenic', '0003_auto_20180508_1055'),
    ]

    operations = [
        migrations.AddField(
            model_name='scenicarea',
            name='about',
            field=models.TextField(default=''),
            preserve_default=False,
        ),
    ]
