# Generated by Django 4.2.4 on 2023-09-08 17:13

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Student', '0025_tuition_ticket_num'),
    ]

    operations = [
        migrations.AddField(
            model_name='tuition',
            name='initial_cost',
            field=models.IntegerField(blank=True, null=True, verbose_name='初期費用'),
        ),
        migrations.AlterField(
            model_name='tuition',
            name='class_count',
            field=models.IntegerField(choices=[(1, '週1回'), (2, '週2回'), (3, 'その他')], default=1, verbose_name='週の回数'),
        ),
    ]
