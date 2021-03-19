# Generated by Django 3.1.6 on 2021-03-13 15:45

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Resturant',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=32, verbose_name='名称')),
                ('longlatitude', models.CharField(max_length=200)),
                ('address', models.CharField(max_length=255, verbose_name='地址')),
                ('res_image', models.ImageField(blank=True, null=True, upload_to='resturants/', verbose_name='图片')),
            ],
            options={
                'verbose_name': '餐厅',
                'verbose_name_plural': '餐厅',
            },
        ),
        migrations.CreateModel(
            name='User',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('username', models.CharField(max_length=32, unique=True, verbose_name='账号')),
                ('password', models.CharField(max_length=32, verbose_name='密码')),
                ('phone', models.CharField(max_length=32, verbose_name='手机号码')),
                ('name', models.CharField(max_length=32, verbose_name='姓名')),
                ('email', models.EmailField(max_length=254, verbose_name='邮箱')),
            ],
            options={
                'verbose_name': '用户',
                'verbose_name_plural': '用户',
            },
        ),
        migrations.CreateModel(
            name='Info',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('mark', models.IntegerField(verbose_name='评分')),
                ('info_time', models.DateTimeField(auto_now_add=True, verbose_name='就餐时间')),
                ('resturant', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='resturants.resturant', verbose_name='餐厅id')),
                ('user', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='resturants.user', verbose_name='用户id')),
            ],
            options={
                'verbose_name': '就餐信息',
                'verbose_name_plural': '就餐信息',
            },
        ),
        migrations.CreateModel(
            name='Comment',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('create_time', models.DateTimeField(auto_now_add=True, verbose_name='评论时间')),
                ('content', models.CharField(default='用户暂未留下评价内容', max_length=255, verbose_name='评论内容')),
                ('resturant', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='resturants.resturant', verbose_name='餐厅id')),
                ('user', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='resturants.user', verbose_name='用户id')),
            ],
            options={
                'verbose_name': '评论',
                'verbose_name_plural': '评论',
            },
        ),
    ]
