# Generated by Django 3.1.6 on 2021-03-17 13:23

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('resturants', '0002_auto_20210314_1530'),
    ]

    operations = [
        migrations.AddField(
            model_name='resturant',
            name='position',
            field=models.CharField(default='暂无', max_length=32, verbose_name='商区'),
        ),
        migrations.AddField(
            model_name='resturant',
            name='rate_service',
            field=models.DecimalField(decimal_places=2, default=5.0, max_digits=3, verbose_name='服务'),
        ),
        migrations.AddField(
            model_name='resturant',
            name='rate_surround',
            field=models.DecimalField(decimal_places=2, default=5.0, max_digits=3, verbose_name='环境'),
        ),
        migrations.AddField(
            model_name='resturant',
            name='rate_taste',
            field=models.DecimalField(decimal_places=2, default=5.0, max_digits=3, verbose_name='口味'),
        ),
        migrations.AddField(
            model_name='resturant',
            name='type',
            field=models.CharField(default='自助餐', max_length=32, verbose_name='类型'),
        ),
    ]