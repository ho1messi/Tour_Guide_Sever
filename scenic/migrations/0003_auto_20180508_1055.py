# Generated by Django 2.0.3 on 2018-05-08 02:55

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('scenic', '0002_auto_20180420_1327'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='scenicspot',
            name='image',
        ),
        migrations.RemoveField(
            model_name='scenicspot',
            name='position',
        ),
    ]