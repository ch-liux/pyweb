# _*_ encoding:utf-8 _*_
from django.urls import path, re_path
from .views import CourseListView, CourseDetailView, CourseInfoView, CourseCommentView, AddCommentView, VideoPlayView

app_name = 'courses'
urlpatterns = [
    # 课程列表
    path('list/', CourseListView.as_view(), name="courses_list"),
    # 课程详情
    re_path('detail/(?P<course_id>\d+)', CourseDetailView.as_view(), name="courses_detail"),
    # 课程学习
    re_path('info/(?P<course_id>\d+)', CourseInfoView.as_view(), name="courses_info"),
    # 课程评论
    re_path('comment/(?P<course_id>\d+)', CourseCommentView.as_view(), name="courses_comment"),
    # 新增评论
    path('add_comment/', AddCommentView.as_view(), name="courses_add_comment"),
    # 视频播放
    re_path('video/(?P<video_id>\d+)', VideoPlayView.as_view(), name="video_play"),
]
