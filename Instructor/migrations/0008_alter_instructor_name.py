# Generated by Django 3.2.9 on 2023-05-22 14:58

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Instructor', '0007_auto_20230522_2341'),
    ]

    operations = [
        migrations.AlterField(
            model_name='instructor',
            name='name',
            field=models.CharField(default=None, max_length=15, null=True, verbose_name='講師名'),
        ),
    ]
