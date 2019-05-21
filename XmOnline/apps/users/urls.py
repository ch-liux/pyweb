# _*_ encoding:utf-8 _*_
from django.urls import path, re_path
from .views import UserInfoView, UserImageUpload, UserModifyPwdView, SendEmailCodeView, \
    UpdateEmailView, MyCourseView, MyFavOrgView, MyFavTeacherView, MyFavCourseView, MyMeassageView

app_name = 'users'
urlpatterns = [
    # 用户信息
    path('info/', UserInfoView.as_view(), name="user_info"),

    # 头像
    path('image/upload/', UserImageUpload.as_view(), name="image_upload"),

    # 修改密码
    path('update/pwd/', UserModifyPwdView.as_view(), name="update_pwd"),

    # 发送邮箱验证码
    path('sendemail_code/', SendEmailCodeView.as_view(), name="sendemail_code"),

    # 修改邮箱
    path('update_email/', UpdateEmailView.as_view(), name="update_email"),

    # 我的课程
    path('mycourse/', MyCourseView.as_view(), name="mycourse"),

    # 我的收藏机构
    path('myfav/org/', MyFavOrgView.as_view(), name="myfav_org"),

    # 我的收藏教师
    path('myfav/teacher/', MyFavTeacherView.as_view(), name="myfav_teacher"),

    # 我的收藏课程
    path('myfav/course/', MyFavCourseView.as_view(), name="myfav_course"),

    # 我的收藏课程
    path('mymessage', MyMeassageView.as_view(), name="mymessage"),


]
