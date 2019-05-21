# _*_ encoding:utf-8 _*_
from django.shortcuts import render
from django.views.generic import View
from django.http import HttpResponse
from django.db.models import Q

from .models import Course, CourseResource, Video
from apps.operation.models import UserFavorate, CourseComments, UserCourse
from apps.utils.mixin_utils import LoginRequiredMixin

from pure_pagination import Paginator, PageNotAnInteger


class CourseListView(View):
    def get(self, request):
        all_course = Course.objects.all().order_by("-add_time")
        # 热门课程
        hot_orgs = all_course.order_by("-click_num")[:3]
        # 关键字
        search_keywords = request.GET.get("keywords", "")
        if search_keywords:
            all_course = all_course.filter(Q(name__icontains=search_keywords) |
                                           Q(desc__icontains=search_keywords) |
                                           Q(detail__icontains=search_keywords))
        # 排序
        sort = request.GET.get('sort', "")
        if sort:
            if sort == "students":
                all_course = all_course.order_by("-students")
            elif sort == "hot":
                all_course = all_course.order_by("-click_num")
        # 分页
        try:
            page = request.GET.get('page', 1)
        except PageNotAnInteger:
            page = 1
        p = Paginator(all_course, 6, request=request)
        course = p.page(page)
        current_nav = 'course'
        return render(request, 'course-list.html', {"all_course": course,
                                                    "hot_orgs": hot_orgs,
                                                    "sort": sort,
                                                    'current_nav': current_nav
                                                    })


class CourseDetailView(View):
    def get(self, request, course_id):
        course = Course.objects.get(id=int(course_id))
        course.click_num += 1
        course.save()   # 增加课程点击数
        # 相关课程
        tag = course.tag
        relate_course = []
        if tag:
            relate_course = Course.objects.filter(tag=tag).exclude(id=course.id)[:1]
        # 收藏
        has_fav1 = False
        has_fav2 = False
        if request.user.is_authenticated:
            if UserFavorate.objects.filter(user=request.user, fav_id=course.id, fav_type=1):
                has_fav1 = True
            if UserFavorate.objects.filter(user=request.user, fav_id=course.course_org_id, fav_type=2):
                has_fav2 = True
        return render(request, 'course-detail.html', {"course": course,
                                                      "has_fav1": has_fav1,
                                                      "has_fav2": has_fav2,
                                                      "relate_course": relate_course})


class CourseInfoView(LoginRequiredMixin, View):
    def get(self, request, course_id):
        course = Course.objects.get(id=int(course_id))
        course.students += 1
        course.save()
        # 查询用户是否关联课程
        user_courses = UserCourse.objects.filter(user=request.user, course=course)
        if not user_courses:
            user_course = UserCourse(user=request.user, course=course)
            user_course.save()
        # 学过课程的学生
        user_cousers = UserCourse.objects.filter(course=course)
        user_ids = [user_couser.user.id for user_couser in user_cousers]
        all_user_course = UserCourse.objects.filter(user_id__in=user_ids)
        # 取出所有课程id
        course_ids = [user_couser.course.id for user_couser in all_user_course]
        # 获取相关用户的课程
        relate_course = Course.objects.filter(id__in=course_ids).exclude(id=course.id).order_by('-click_num')[:5]
        # 资料
        all_resource = CourseResource.objects.filter(course=course)
        return render(request, "course-video.html", {"course": course,
                                                     "all_resource": all_resource,
                                                     "relate_course": relate_course})


class CourseCommentView(LoginRequiredMixin, View):
    def get(self, request, course_id):
        course = Course.objects.get(id=int(course_id))
        all_resource = CourseResource.objects.filter(course=course)
        all_comments = CourseComments.objects.filter(course=course)
        return render(request, "course-comment.html", {"course": course,
                                                       "all_resource": all_resource,
                                                       "all_comments": all_comments})


class AddCommentView(LoginRequiredMixin, View):
    def post(self, request):
        if not request.user.is_authenticated:
            return HttpResponse('{"status":"fail", "msg":"用户未登录"}', content_type='application/json')
        course_id = request.POST.get('course_id', 0)
        comments = request.POST.get('comments', '')
        if int(course_id) > 0 and comments:
            course_comments = CourseComments()
            course = Course.objects.get(id=int(course_id))
            course_comments.course_id = course.id
            course_comments.comments = comments
            course_comments.user = request.user
            course_comments.save()
            return HttpResponse('{"status":"success", "msg":"添加成功"}', content_type='application/json')
        else:
            return HttpResponse('{"status":"fail", "msg":"添加失败"}', content_type='application/json')


class VideoPlayView(View):
    # 视频播放
    def get(self, request, video_id):
        video = Video.objects.get(id=int(video_id))
        course = video.lesson.course
        # 查询用户是否关联课程
        user_courses = UserCourse.objects.filter(user=request.user, course=course)
        if not user_courses:
            user_course = UserCourse(user=request.user, course=course)
            user_course.save()
        # 学过课程的学生
        user_cousers = UserCourse.objects.filter(course=course)
        user_ids = [user_couser.user.id for user_couser in user_cousers]
        all_user_course = UserCourse.objects.filter(user_id__in=user_ids)
        # 取出所有课程id
        course_ids = [user_couser.course.id for user_couser in all_user_course]
        # 获取相关用户的课程
        relate_course = Course.objects.filter(id__in=course_ids).exclude(id=course.id).order_by('-click_num')[:5]
        # 资料
        all_resource = CourseResource.objects.filter(course=course)
        return render(request, "course-play.html", {"course": course,
                                                     "all_resource": all_resource,
                                                     "relate_course": relate_course,
                                                     "video": video})
