# Generated by Django 5.0.3 on 2024-04-01 20:39

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('my_scheduler_api', '0002_employee_workdays'),
    ]

    operations = [
        migrations.AlterField(
            model_name='appointment',
            name='date',
            field=models.CharField(max_length=100),
        ),
        migrations.AlterField(
            model_name='appointment',
            name='time',
            field=models.CharField(max_length=100),
        ),
    ]
