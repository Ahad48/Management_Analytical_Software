# Generated by Django 3.0.5 on 2021-03-01 15:58

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('hr', '0001_initial'),
    ]

    operations = [
        migrations.RenameField(
            model_name='attendance',
            old_name='employee',
            new_name='Employee_id',
        ),
        migrations.AddField(
            model_name='employee',
            name='employee_id',
            field=models.CharField(default='', max_length=10, unique=True),
        ),
    ]
