# Generated by Django 3.0.5 on 2021-03-01 16:27

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('hr', '0004_auto_20210301_2154'),
    ]

    operations = [
        migrations.AlterField(
            model_name='attendance',
            name='Employee_id',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to='hr.Employee'),
        ),
        migrations.AlterField(
            model_name='employee',
            name='department_name',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to='hr.Department'),
        ),
        migrations.AlterField(
            model_name='employeeskillchart',
            name='Employee_id',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to='hr.Employee'),
        ),
    ]
