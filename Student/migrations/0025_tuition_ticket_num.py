# Generated by Django 4.2.4 on 2023-08-21 14:02

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Student', '0024_external_tuition_ticket_num'),
    ]

    operations = [
        migrations.AddField(
            model_name='tuition',
            name='ticket_num',
            field=models.IntegerField(blank=True, default=0, null=True, verbose_name='チケットの購入枚数'),
        ),
    ]
