# _*_ encoding:utf-8 _*_
from django.urls import path, re_path

from .views import OrgView, AddUserAskView, OrgHomeView, OrgCourseView, OrgDescView, \
    OrgTeacherView, AddFavView, TeacherListView, TeacherDetailView

app_name = 'org'
urlpatterns = [
    # 课程机构首页
    path('list/', OrgView.as_view(), name="org_list"),
    # 添加询问
    path('add_ask/', AddUserAskView.as_view(), name="add_ask"),
    # 机构首页
    re_path('home/(?P<org_id>\d+)/', OrgHomeView.as_view(), name="org_home"),
    # 课程机构
    re_path('course/(?P<org_id>\d+)/', OrgCourseView.as_view(), name="org_course"),
    # 机构简介
    re_path('desc/(?P<org_id>\d+)/', OrgDescView.as_view(), name="org_desc"),
    # 机构教师
    re_path('teacher/(?P<org_id>\d+)/', OrgTeacherView.as_view(), name="org_teacher"),
    # 机构收藏
    re_path('add_fav/', AddFavView.as_view(), name="add_fav"),
    # 讲师列表页
    path('teacher/list/', TeacherListView.as_view(), name="teacher_list"),
    # 讲师详情页
    re_path('teacher/detail/(?P<teacher_id>\d+)/', TeacherDetailView.as_view(), name="teacher_detail")
]
