# Generated by Django 3.0.5 on 2021-03-01 16:04

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('hr', '0002_auto_20210301_2128'),
    ]

    operations = [
        migrations.AlterField(
            model_name='employee',
            name='error',
            field=models.FloatField(),
        ),
        migrations.AlterField(
            model_name='employee',
            name='performance_score',
            field=models.FloatField(),
        ),
    ]