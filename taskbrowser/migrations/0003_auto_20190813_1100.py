# Generated by Django 2.2.4 on 2019-08-13 10:00

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('taskbrowser', '0002_auto_20190813_1011'),
    ]

    operations = [
        migrations.AlterField(
            model_name='task',
            name='priority',
            field=models.IntegerField(),
        ),
        migrations.AlterField(
            model_name='task',
            name='taskowner',
            field=models.CharField(max_length=30),
        ),
    ]