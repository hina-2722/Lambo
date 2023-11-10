# Generated by Django 3.2.9 on 2023-05-22 14:41

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Instructor', '0006_auto_20230522_2218'),
    ]

    operations = [
        migrations.AddField(
            model_name='instructor',
            name='birth_date',
            field=models.DateField(blank=True, null=True, verbose_name='生年月日'),
        ),
        migrations.AddField(
            model_name='instructor',
            name='instructor_id',
            field=models.CharField(max_length=6, null=True, unique=True),
        ),
        migrations.AddField(
            model_name='instructor',
            name='last_login',
            field=models.DateTimeField(blank=True, null=True, verbose_name='last login'),
        ),
        migrations.AddField(
            model_name='instructor',
            name='password',
            field=models.CharField(default='20210927', max_length=128),
        ),
        migrations.AlterField(
            model_name='instructor',
            name='name',
            field=models.CharField(default=None, max_length=15, verbose_name='講師名'),
        ),
    ]
