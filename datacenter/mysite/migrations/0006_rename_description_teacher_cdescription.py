# Generated by Django 5.0.4 on 2024-07-08 07:43

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('mysite', '0005_teacher_ccourse'),
    ]

    operations = [
        migrations.RenameField(
            model_name='teacher',
            old_name='description',
            new_name='cdescription',
        ),
    ]
