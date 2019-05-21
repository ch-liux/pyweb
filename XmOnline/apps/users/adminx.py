# -*- coding: utf-8 -*-
__author__ = 'lx'
__date__ = '2018/10/7 16:30'

import xadmin
from xadmin import views

from .models import EmailVerifyRecord, Banner


# 主题
class BaseSetting(object):
    enable_themes = True
    use_bootswatch = True


# 全局变量
class GlobalSetting(object):
    site_title = "慕学后台管理系统"
    site_footer = "慕学在线网"
    # 左列菜单
    menu_style = "accordion"


class EmailVerifyRecordAdmin(object):
    list_display = ['code', 'email', 'send_type', 'send_time']
    search_fields = ['code', 'email', 'send_type']
    list_filter = ['code', 'email', 'send_type', 'send_time']
    model_icon = 'fa fa-address-book-o'


class BannerAdmin(object):
    # 显示字段列
    list_display = ['title', 'image', 'url', 'index', 'add_time']
    # 搜索
    search_fields = ['title', 'image', 'url', 'index']
    # 过滤器
    list_filter = ['title', 'image', 'url', 'index', 'add_time']


xadmin.site.register(EmailVerifyRecord, EmailVerifyRecordAdmin)
xadmin.site.register(Banner, BannerAdmin)
xadmin.site.register(views.BaseAdminView, BaseSetting)
xadmin.site.register(views.CommAdminView, GlobalSetting)