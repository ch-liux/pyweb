# Generated by Django 2.1.2 on 2018-10-20 16:47

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('courses', '0009_auto_20181020_1642'),
    ]

    operations = [
        migrations.AlterField(
            model_name='course',
            name='image',
            field=models.ImageField(blank=True, null=True, upload_to='courses/%Y/%m', verbose_name='封面图'),
        ),
    ]