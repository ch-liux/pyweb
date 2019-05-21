# _*_ encoding:utf-8 _*_
"""XmOnline URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/2.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""

from django.urls import path, include, re_path
from django.views.static import serve
from django.contrib import admin
from xadmin.plugins import xversion
from apps.users.views import LoginView, RegisterView, AciveUserView, \
                            ForgetPasswordView, RestView, ModifyPwdView, LogoutView, IndexView
from XmOnline import settings
import xadmin
from django.conf.urls.static import static

xadmin.autodiscover()
xversion.register_models()

urlpatterns = [
    # 后台
    path('xadmin/', xadmin.site.urls),
    path('admin/', admin.site.urls),
    # 首页
    path('', IndexView.as_view(), name="index"),
    # 登录
    path('login/', LoginView.as_view(), name="login"),
    # 退出
    path('logout/', LogoutView.as_view(), name="logout"),
    # 注册
    path('register/', RegisterView.as_view(), name="register"),
    # 图片验证码
    path('captcha/', include('captcha.urls')),
    # 激活
    re_path('^active/(?P<active_code>.*)/', AciveUserView.as_view(), name="user_active"),
    # 忘记密码
    path('forget/', ForgetPasswordView.as_view(), name="forget_pwd"),
    # 重置密码激活
    re_path('^reset/(?P<active_code>.*)/', RestView.as_view(), name="reset_pwd"),
    # 修改密码
    path('modify_pwd/', ModifyPwdView.as_view(), name="modify_pwd"),

    # 课程机构url
    path('org/', include('apps.organization.urls', namespace='org')),

    # 课程列表url
    path('courses/', include('apps.courses.urls', namespace='courses')),

    # 处理media信息,前台展示(文件访问)
    re_path('^media/(?P<path>.*)', serve, {"document_root": settings.MEDIA_ROOT}),

    # 用户中心
    path('users/', include('apps.users.urls', namespace='users')),

    # 部署时静态文件转发
    re_path('static/(?P<path>.*)', serve, {"document_root": settings.STATIC_ROOT}, name='static'),

    # ueditor
    path('ueditor/', include('DjangoUeditor.urls')),
]

# 全局404
handler404 = 'apps.users.views.page_not_found'
handler500 = 'apps.users.views.page_error'
