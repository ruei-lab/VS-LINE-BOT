# Generated by Django 5.0.4 on 2024-07-10 07:56

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('mysite', '0006_rename_description_teacher_cdescription'),
    ]

    operations = [
        migrations.CreateModel(
            name='AlbumModel',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('adate', models.DateTimeField(auto_now=True)),
                ('alocation', models.CharField(blank=True, default='', max_length=200)),
                ('atitle', models.TextField(blank=True, default='')),
            ],
        ),
        migrations.CreateModel(
            name='PhotoModel',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('psubject', models.CharField(max_length=100)),
                ('pdate', models.DateTimeField(auto_now=True)),
                ('purl', models.CharField(max_length=100)),
                ('phit', models.IntegerField(default=0)),
                ('palbum', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='mysite.albummodel')),
            ],
        ),
    ]
