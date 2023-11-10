# Generated by Django 3.2.9 on 2023-05-20 12:30

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('Instructor', '0001_initial'),
        ('Student', '0012_alter_project_status'),
    ]

    operations = [
        migrations.CreateModel(
            name='Reservation',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('datetime', models.DateTimeField()),
                ('instructor', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='instructor_reservations', to='Instructor.instructor')),
                ('student', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='student_reservations', to='Student.student')),
            ],
        ),
    ]
