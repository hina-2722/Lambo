# Generated by Django 4.2.1 on 2023-06-08 11:12

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('Instructor', '0020_alter_timeslot_options'),
        ('Reservation', '0006_delete_todaylesson'),
    ]

    operations = [
        migrations.AlterField(
            model_name='reservation',
            name='schedule',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='Instructor.schedule', verbose_name='スケジュール'),
        ),
    ]
