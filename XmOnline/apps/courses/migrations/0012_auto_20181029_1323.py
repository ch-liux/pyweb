# Generated by Django 2.1.2 on 2018-10-29 13:23

import DjangoUeditor.models
from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('courses', '0011_course_is_banner'),
    ]

    operations = [
        migrations.AlterField(
            model_name='course',
            name='desc',
            field=DjangoUeditor.models.UEditorField(default='', verbose_name='课程描述'),
        ),
    ]
