# Generated by Django 2.1.2 on 2018-10-27 17:52

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('courses', '0010_auto_20181020_1647'),
    ]

    operations = [
        migrations.AddField(
            model_name='course',
            name='is_banner',
            field=models.BooleanField(default=False, verbose_name='是否广告轮播'),
        ),
    ]
