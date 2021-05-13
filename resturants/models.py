from django.db import models


# Create your models here.


class User(models.Model):
    username = models.CharField(max_length=32, verbose_name='账号')
    password = models.CharField(max_length=32, verbose_name='密码', default='123456')
    phone = models.CharField(max_length=32, null=True, blank=True, verbose_name='手机号码')
    name = models.CharField(max_length=32, null=True, blank=True, verbose_name='姓名')
    email = models.EmailField(verbose_name='邮箱', blank=True, null=True)

    class Meta:
        verbose_name = '用户'
        verbose_name_plural = '用户'

    def __str__(self):
        return self.username


class Resturant(models.Model):
    name = models.CharField(max_length=200, verbose_name='名称')
    longlatitude = models.CharField(max_length=200, null=True, blank=True, verbose_name='编号')
    longtitude = models.DecimalField(max_digits=12, decimal_places=9, null=True, blank=True, verbose_name="经度")
    latitude = models.DecimalField(max_digits=12, decimal_places=9, null=True, blank=True, verbose_name="纬度")
    address = models.CharField(max_length=255, verbose_name='地址')
    type = models.CharField(max_length=32, default="自助餐", verbose_name="类型")
    position = models.CharField(max_length=32, null=True, blank=True, verbose_name="商区")
    rate_taste = models.DecimalField(max_digits=3,decimal_places=2, default=5.00, verbose_name="口味")
    rate_surround = models.DecimalField(max_digits=3,decimal_places=2, default=5.00, verbose_name="环境")
    rate_service = models.DecimalField(max_digits=3,decimal_places=2, default=5.00, verbose_name="服务")
    res_image = models.ImageField(upload_to='resturants/', null=True, blank=True, verbose_name='图片')

    class Meta:
        verbose_name = '餐厅'
        verbose_name_plural = '餐厅'

    def __str__(self):
        return self.name


# 记录就餐信息
class Info(models.Model):
    resturant = models.ForeignKey(
        Resturant, on_delete=models.CASCADE, blank=True, null=True, verbose_name='餐厅id'
    )
    user = models.ForeignKey(
        User, on_delete=models.CASCADE, blank=True, null=True, verbose_name='用户id'
    )

    info_time = models.DateTimeField(verbose_name='就餐时间', auto_now_add=True)

    class Meta:
        verbose_name = '就餐信息'
        verbose_name_plural = '就餐信息'

# 记录用户的评价信息，作为后续系统的改进
class Comment(models.Model):
    resturant = models.ForeignKey(
        Resturant, on_delete=models.CASCADE, blank=True, null=True, verbose_name='餐厅id'
    )
    user = models.ForeignKey(
        User, on_delete=models.CASCADE, blank=True, null=True, verbose_name='用户id'
    )
    rate_taste = models.DecimalField(max_digits=3, decimal_places=2, default=5.00, verbose_name="口味")
    rate_surround = models.DecimalField(max_digits=3, decimal_places=2, default=5.00, verbose_name="环境")
    rate_service = models.DecimalField(max_digits=3, decimal_places=2, default=5.00, verbose_name="服务")
    create_time = models.DateTimeField(auto_now_add=True, verbose_name='评论时间')
    content = models.CharField(max_length=255, default="用户暂未留下评价内容", verbose_name="评论内容")

    class Meta:
        verbose_name = "评论"
        verbose_name_plural = '评论'

