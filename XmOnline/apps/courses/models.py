# _*_ encoding:utf-8 _*_
from django.db import models

from apps.organization.models import CourseOrg, Teacher
from DjangoUeditor.models import UEditorField

from datetime import datetime
# Create your models here.


class Course(models.Model):
    course_org = models.ForeignKey(CourseOrg, verbose_name="课程机构", on_delete=models.CASCADE, null=True, blank=True)
    name = models.CharField(verbose_name="课程名", max_length=50)
    desc = models.CharField(verbose_name="课程描述", max_length=300)
    detail = UEditorField(verbose_name="课程详情", width=600, height=300, imagePath="courses/ueditor/",
                          filePath="courses/ueditor/", default='')
    # detail = models.TextField(verbose_name="课程详情")
    degree = models.CharField(verbose_name="课程难度", choices=(("cj", "初级"), ("zj", "中级"), ("gj", "高级")),
                              max_length=2)
    teacher = models.ForeignKey(Teacher, verbose_name="讲师", null=True, blank=True, on_delete=models.CASCADE)
    learn_times = models.IntegerField(verbose_name="学习时长(分钟数)", default=0)
    students = models.IntegerField(verbose_name="学习人数", default=0)
    fav_nums = models.IntegerField(verbose_name="收藏数", default=0)
    image = models.ImageField(verbose_name="封面图", upload_to="courses/%Y/%m", max_length=100, null=True, blank=True)
    click_num = models.IntegerField(verbose_name="点击数", default=0)
    category = models.CharField(verbose_name="课程类别", max_length=20, default="后端开发")
    tag = models.CharField(verbose_name="课程标签", max_length=10, default='')
    need_know = models.CharField(verbose_name="课程须知", max_length=300, default='')
    teacher_tell = models.CharField(verbose_name="老师告诉你", max_length=300, default='')
    is_banner = models.BooleanField(verbose_name="是否广告轮播", default=False)
    add_time = models.DateField(verbose_name="添加时间", default=datetime.now)

    class Meta:
        verbose_name = "课程"
        verbose_name_plural = verbose_name

    # 获取课程章节数
    def get_zj_count(self):
        return self.lesson_set.all().count()

    # 获取学习用户
    def get_user_count(self):
        return self.usercourse_set.all()[:5]

    # 获取课程章节
    def get_all_zj(self):
        return self.lesson_set.all()

    def __str__(self):
        return self.name


class Lesson(models.Model):
    course = models.ForeignKey(Course, on_delete=models.CASCADE, verbose_name="课程")
    name = models.CharField(max_length=100, verbose_name="章节名")
    add_time = models.DateField(verbose_name="添加时间", default=datetime.now)

    class Meta:
        verbose_name = "章节"
        verbose_name_plural = verbose_name

    # 获取课程章节视频
    def get_all_zj_video(self):
        return self.video_set.all()

    def __str__(self):
        return self.name


class Video(models.Model):
    lesson = models.ForeignKey(Lesson, on_delete=models.CASCADE, verbose_name="章节名")
    name = models.CharField(max_length=100, verbose_name="视频名")
    url = models.CharField(max_length=200, verbose_name="访问地址", default="")
    learn_times = models.IntegerField(verbose_name="时长(分钟数)", default=0)
    add_time = models.DateField(verbose_name="添加时间", default=datetime.now)

    class Meta:
        verbose_name = "视频"
        verbose_name_plural = verbose_name

    def __str__(self):
        return self.name


class CourseResource(models.Model):
    course = models.ForeignKey(Course, on_delete=models.CASCADE, verbose_name="课程")
    name = models.CharField(max_length=100, verbose_name="名称")
    download = models.FileField(verbose_name="资源文件", upload_to="course/resource/%Y/%m", max_length=100)
    add_time = models.DateField(verbose_name="添加时间", default=datetime.now)

    class Meta:
        verbose_name = "课程资源"
        verbose_name_plural = verbose_name

    def __str__(self):
        return self.name
