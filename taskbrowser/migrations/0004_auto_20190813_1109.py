# Generated by Django 2.2.4 on 2019-08-13 10:09

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('taskbrowser', '0003_auto_20190813_1100'),
    ]

    operations = [
        migrations.AlterField(
            model_name='task',
            name='priority',
            field=models.IntegerField(default=1),
        ),
        migrations.AlterField(
            model_name='task',
            name='taskowner',
            field=models.CharField(default='noowner', max_length=30),
        ),
    ]
