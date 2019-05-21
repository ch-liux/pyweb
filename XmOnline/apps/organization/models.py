# _*_ encoding:utf-8 _*_
from django.db import models
from datetime import datetime
# Create your models here.


class CityDict(models.Model):
    name = models.CharField(verbose_name="城市名称", max_length=20)
    desc = models.CharField(verbose_name="描述", max_length=200)
    add_time = models.DateField(verbose_name="添加时间", default=datetime.now)

    class Meta:
        verbose_name = "城市"
        verbose_name_plural = verbose_name

    def __str__(self):
        return self.name


class CourseOrg(models.Model):
    name = models.CharField(verbose_name="机构名称", max_length=50)
    desc = models.TextField(verbose_name="机构描述")
    tag = models.CharField(verbose_name="机构标签", max_length=4, default='全国知名')
    catgory = models.CharField(verbose_name="机构类别", max_length=20, default="pxjg",
                               choices=(("pxjg", "培训结构"), ("gr", "个人"), ("gx", "高校")))
    click_nums = models.IntegerField(verbose_name="点击次数", default=0)
    fav_nums = models.IntegerField(verbose_name="收藏数", default=0)
    image = models.ImageField(verbose_name="logo", upload_to="org/%Y/%m", max_length=100)
    address = models.CharField(verbose_name="机构地址", max_length=150)
    city = models.ForeignKey(CityDict, on_delete=models.CASCADE, verbose_name="城市")
    students = models.IntegerField(default=0, verbose_name="学习人数")
    course_nums = models.IntegerField(default=0, verbose_name="课程数")
    add_time = models.DateField(verbose_name="添加时间", default=datetime.now)

    class Meta:
        verbose_name = "课程机构"
        verbose_name_plural = verbose_name

    def get_teacher_count(self):
        return self.teacher_set.count()

    def __str__(self):
        return self.name


class Teacher(models.Model):
    org = models.ForeignKey(CourseOrg, on_delete=models.CASCADE, verbose_name="所属机构")
    name = models.CharField(verbose_name="教师名称", max_length=50)
    age = models.IntegerField(verbose_name="年龄", default=18)
    work_years = models.IntegerField(verbose_name="工作年限", default=0)
    work_company = models.CharField(verbose_name="就职公司", max_length=50)
    work_position = models.CharField(verbose_name="公司职位", max_length=50)
    points = models.CharField(verbose_name="教学特点", max_length=50)
    click_nums = models.IntegerField(verbose_name="点击次数", default=0)
    fav_nums = models.IntegerField(verbose_name="收藏数", default=0)
    image = models.ImageField(verbose_name="头像", upload_to="teacher/%Y/%m", max_length=100, default='')
    add_time = models.DateField(verbose_name="添加时间", default=datetime.now)

    class Meta:
        verbose_name = "教师"
        verbose_name_plural = verbose_name

    def get_course_count(self):
        return self.course_set.count()

    def __str__(self):
        return self.name
