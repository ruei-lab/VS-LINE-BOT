# Generated by Django 5.0.4 on 2024-07-22 07:22

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('mysite', '0010_teacher_cgrade_teacher_csemmester'),
    ]

    operations = [
        migrations.RenameField(
            model_name='teacher',
            old_name='csemmester',
            new_name='csemester',
        ),
    ]
