# Generated by Django 5.0.4 on 2024-07-30 05:56

import django.utils.timezone
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('mysite', '0012_alter_teacher_cgender'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='photo',
            name='title',
        ),
        migrations.AddField(
            model_name='photo',
            name='upload_data',
            field=models.DateField(default=django.utils.timezone.now),
        ),
        migrations.AlterField(
            model_name='photo',
            name='image',
            field=models.ImageField(upload_to='image/'),
        ),
    ]
