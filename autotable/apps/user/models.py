from django.db import models
from django.contrib.auth.models import AbstractUser


# 继承django默认的用户表并加入字段
class UserProfile(AbstractUser):
    gender_c = (("male", "男"), ("female", "女"))
    nickname = models.CharField(max_length=50, default="", null=True, blank=True, verbose_name="昵称")
    birthday = models.DateField(null=True, blank=True, verbose_name="生日")
    gender = models.CharField(choices=gender_c, default="female", max_length=7, verbose_name="性别")
    address = models.CharField(max_length=100, null=True, blank=True, default="", verbose_name="地址")
    mobile = models.CharField(max_length=11, null=True, blank=True, verbose_name="联系方式")
    desc = models.CharField(max_length=200, null=True, blank=True, verbose_name="备注")

    class Meta:
        db_table = 'at_user'
        verbose_name = "用户信息"
        verbose_name_plural = verbose_name
