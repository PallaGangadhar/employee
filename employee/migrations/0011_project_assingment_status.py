# Generated by Django 2.1.7 on 2019-03-05 05:38

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('employee', '0010_auto_20190227_0637'),
    ]

    operations = [
        migrations.AddField(
            model_name='project_assingment',
            name='status',
            field=models.CharField(choices=[('complete', 'Complete'), ('incomplete', 'Incomplete'), ('running', 'Running')], default='incomplete', max_length=128),
        ),
    ]
