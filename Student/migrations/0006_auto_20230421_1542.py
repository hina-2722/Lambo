# Generated by Django 3.2.9 on 2023-04-21 06:42

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Student', '0005_absence'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='tuition',
            options={'verbose_name': '月謝', 'verbose_name_plural': '月謝管理'},
        ),
        migrations.AddField(
            model_name='tuition',
            name='age_group',
            field=models.CharField(blank=True, choices=[('小学生', '小学生'), ('中学生', '中学生'), ('高校生', '高校生')], max_length=10, null=True, verbose_name='年齢グループ'),
        ),
        migrations.AddField(
            model_name='tuition',
            name='class_count',
            field=models.IntegerField(choices=[(1, '週1回'), (2, '週2回')], default=1, verbose_name='週の回数'),
        ),
        migrations.AddField(
            model_name='tuition',
            name='due_date',
            field=models.DateField(blank=True, null=True, verbose_name='支払い期限'),
        ),
        migrations.AlterField(
            model_name='tuition',
            name='payment_status',
            field=models.CharField(choices=[('未払い', '未払い'), ('済み', '済み'), ('調整中', '調整中'), ('払い戻し済み', '払い戻し済み')], default='未払い', max_length=10, verbose_name='支払い状況'),
        ),
    ]
