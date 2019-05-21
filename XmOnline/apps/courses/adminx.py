# -*- coding: utf-8 -*-
__author__ = 'lx'
__date__ = '2018/10/7 16:30'

import xadmin

from .models import Lesson, Video, CourseResource, Course


class CourseAdmin(object):
    # 显示字段列
    list_display = ['name', 'desc', 'detail', 'degree', 'learn_times', 'students',
                    'fav_nums', 'image', 'click_num', 'add_time']
    # 搜索
    search_fields = ['name', 'desc', 'detail', 'degree', 'learn_times', 'students', 'fav_nums', 'image', 'click_num']
    # 过滤器
    list_filter = ['name', 'desc', 'detail', 'degree', 'learn_times', 'students',
                   'fav_nums', 'image', 'click_num', 'add_time']
    style_fields = {"detail": "ueditor"}


class LessonAdmin(object):
    list_display = ['course', 'name', 'add_time']
    search_fields = ['course', 'name']
    list_filter = ['course__name', 'name', 'add_time']


class VideoAdmin(object):
    list_display = ['lesson', 'name', 'add_time']
    search_fields = ['lesson', 'name']
    list_filter = ['lesson', 'name', 'add_time']


class CourseResourceAdmin(object):
    list_display = ['course', 'name', 'download', 'add_time']
    search_fields = ['course', 'name']
    list_filter = ['course', 'name', 'download', 'add_time']


xadmin.site.register(Course, CourseAdmin)
xadmin.site.register(Lesson, LessonAdmin)
xadmin.site.register(Video, VideoAdmin)
xadmin.site.register(CourseResource, CourseResourceAdmin)