# Generated by Django 2.1.5 on 2019-02-27 06:37

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('employee', '0009_auto_20190227_0628'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='project_assingment',
            name='staff',
        ),
        migrations.AddField(
            model_name='project_assingment',
            name='emp',
            field=models.ForeignKey(default='', on_delete=django.db.models.deletion.CASCADE, to='employee.employee'),
        ),
    ]
