# Generated by Django 5.0.4 on 2024-07-22 07:35

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('mysite', '0011_rename_csemmester_teacher_csemester'),
    ]

    operations = [
        migrations.AlterField(
            model_name='teacher',
            name='cGender',
            field=models.CharField(default='M', max_length=4),
        ),
    ]
