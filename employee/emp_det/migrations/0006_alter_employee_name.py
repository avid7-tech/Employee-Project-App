# Generated by Django 5.0.7 on 2024-07-29 12:26

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('emp_det', '0005_alter_employee_phone'),
    ]

    operations = [
        migrations.AlterField(
            model_name='employee',
            name='name',
            field=models.CharField(max_length=240),
        ),
    ]
