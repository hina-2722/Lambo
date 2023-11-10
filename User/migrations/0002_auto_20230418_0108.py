# Generated by Django 3.2.9 on 2023-04-17 16:08

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('User', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='user',
            name='parent_first_name',
            field=models.CharField(blank=True, max_length=20, null=True, verbose_name='保護者の苗字'),
        ),
        migrations.AddField(
            model_name='user',
            name='parent_last_name',
            field=models.CharField(blank=True, max_length=20, null=True, verbose_name='保護者の名前'),
        ),
        migrations.AddField(
            model_name='user',
            name='parent_tel',
            field=models.CharField(blank=True, max_length=12, null=True, verbose_name='緊急連絡先'),
        ),
    ]
