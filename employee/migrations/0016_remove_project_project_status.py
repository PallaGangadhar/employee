# Generated by Django 2.1.5 on 2019-03-08 07:00

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('employee', '0015_auto_20190308_0651'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='project',
            name='project_status',
        ),
    ]
