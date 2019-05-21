# _*_ encoding:utf-8 _*_

from django.shortcuts import render
from django.views.generic import View
from django.http import HttpResponse
from .models import CityDict, Teacher, CourseOrg
from django.db.models import Q

from pure_pagination import Paginator, PageNotAnInteger
from .forms import UserAskForm
from apps.operation.models import UserFavorate
from apps.courses.models import Course


class OrgView(View):
    """
    课程机构列表功能
    """
    def get(self, request):
        all_orgs = CourseOrg.objects.all()
        all_citys = CityDict.objects.all()
        # 关键字
        search_keywords = request.GET.get("keywords", "")
        if search_keywords:
            all_orgs = all_orgs.filter(Q(name__icontains=search_keywords) |
                                       Q(desc__icontains=search_keywords))
        # 排序
        sort = request.GET.get('sort', "")
        if sort:
            if sort == "students":
                all_orgs = all_orgs.order_by("-students")
            elif sort == "courses":
                all_orgs = all_orgs.order_by("-course_nums")
        # 授课机构排名
        hot_orgs = all_orgs.order_by("-click_nums")[:3]
        # 分页
        city_id = request.GET.get('city', "")
        if city_id:
            all_orgs = all_orgs.filter(city_id=int(city_id))
        catgory = request.GET.get('ct', "")
        if catgory:
            all_orgs = all_orgs.filter(catgory=catgory)
        org_nums = all_orgs.count()
        try:
            page = request.GET.get('page', 1)
        except PageNotAnInteger:
            page = 1
        p = Paginator(all_orgs, 5, request=request)
        orgs = p.page(page)
        current_nav = 'org'
        return render(request, 'org-list.html', {
            "all_orgs": orgs,
            "all_citys": all_citys,
            "org_nums": org_nums,
            "city_id": city_id,
            "catgory": catgory,
            "hot_orgs": hot_orgs,
            "sort": sort,
            "current_nav": current_nav
        })


class AddUserAskView(View):
    # 用户添加咨询
    def post(self, request):
        userask_form = UserAskForm(request.POST)
        if userask_form.is_valid():
            user_ask = userask_form.save(commit=True)
            return HttpResponse('{"status":"success"}', content_type='application/json')
        return HttpResponse('{"status":"fail", "msg":"添加出错"}', content_type='application/json')


class OrgHomeView(View):
    # 机构首页
    def get(self, request, org_id):
        current_page = 'home'
        course_org = CourseOrg.objects.get(id=int(org_id))
        course_org.click_nums += 1
        course_org.save()
        has_fav = False
        if request.user.is_authenticated:
            if UserFavorate.objects.filter(user=request.user, fav_id=course_org.id, fav_type=2):
                has_fav = True
        # 获取外键所有
        all_courses = course_org.course_set.all()[:3]
        all_teaches = course_org.teacher_set.all()[:1]
        return render(request, 'org-detail-homepage.html', {"course_org": course_org,
                                                            "all_courses": all_courses,
                                                            "all_teaches": all_teaches,
                                                            "current_page": current_page,
                                                            "has_fav": has_fav})


class OrgCourseView(View):
    # 机构课程列表页
    def get(self, request, org_id):
        current_page = "course"
        course_org = CourseOrg.objects.get(id=int(org_id))
        has_fav = False
        if request.user.is_authenticated:
            if UserFavorate.objects.filter(user=request.user, fav_id=course_org.id, fav_type=2):
                has_fav = True
        # 获取外键所有
        all_courses = course_org.course_set.all()
        return render(request, 'org-detail-course.html', {"course_org": course_org,
                                                          "all_courses": all_courses,
                                                          "current_page": current_page,
                                                          "has_fav": has_fav})


class OrgDescView(View):
    # 机构简介列表页
    def get(self, request, org_id):
        current_page = "desc"
        course_org = CourseOrg.objects.get(id=int(org_id))
        has_fav = False
        if request.user.is_authenticated:
            if UserFavorate.objects.filter(user=request.user, fav_id=course_org.id, fav_type=2):
                has_fav = True
        return render(request, 'org-detail-desc.html', {"course_org": course_org,
                                                        "current_page": current_page,
                                                        "has_fav": has_fav})


class OrgTeacherView(View):
    # 机构教师列表页
    def get(self, request, org_id):
        current_page = "teacher"
        course_org = CourseOrg.objects.get(id=int(org_id))
        all_teaches = course_org.teacher_set.all()
        has_fav = False
        if request.user.is_authenticated:
            if UserFavorate.objects.filter(user=request.user, fav_id=course_org.id, fav_type=2):
                has_fav = True
        return render(request, 'org-detail-teachers.html', {"current_page": current_page,
                                                            "all_teaches": all_teaches,
                                                            "course_org": course_org,
                                                            "has_fav": has_fav})


class AddFavView(View):
    """用户收藏/取消收藏"""
    def post(self, request):
        fav_id = request.POST.get("fav_id", "0")
        fav_type = request.POST.get("fav_type", "0")
        # 是否登录
        if not request.user.is_authenticated:
            return HttpResponse('{"status":"fail", "msg":"用户未登录"}', content_type='application/json')
        exist_records = UserFavorate.objects.filter(user=request.user, fav_id=int(fav_id), fav_type=int(fav_type))
        if exist_records:
            # 存在取消收藏
            exist_records.delete()
            if int(fav_type) == 1:
                fav_obj = Course.objects.get(id=int(fav_id))
            elif int(fav_type) == 2:
                fav_obj = CourseOrg.objects.get(id=int(fav_id))
            elif int(fav_type) == 3:
                fav_obj = Teacher.objects.get(id=int(fav_id))
            fav_obj.fav_nums -= 1
            if fav_obj.fav_nums < 0:
                fav_obj.fav_nums = 0
            fav_obj.save()
            return HttpResponse('{"status":"success", "msg":"收藏"}', content_type='application/json')
        else:
            user_favorate = UserFavorate()
            if int(fav_id) > 0 and int(fav_type) > 0:
                user_favorate.user = request.user
                user_favorate.fav_id = int(fav_id)
                user_favorate.fav_type = int(fav_type)
                user_favorate.save()

                if int(fav_type) == 1:
                    fav_obj = Course.objects.get(id=int(fav_id))
                elif int(fav_type) == 2:
                    fav_obj = CourseOrg.objects.get(id=int(fav_id))
                elif int(fav_type) == 3:
                    fav_obj = Teacher.objects.get(id=int(fav_id))
                fav_obj.fav_nums += 1
                fav_obj.save()
                return HttpResponse('{"status":"success", "msg":"已收藏"}', content_type='application/json')
            else:
                return HttpResponse('{"status":"fail", "msg":"收藏出错"}', content_type='application/json')


class TeacherListView(View):
    def get(self, request):
        all_teacher = Teacher.objects.all()
        teacher_count = all_teacher.count()
        # 关键字
        search_keywords = request.GET.get("keywords", "")
        if search_keywords:
            all_teacher = all_teacher.filter(Q(name__icontains=search_keywords) |
                                             Q(work_company__icontains=search_keywords))
        # 人气
        sort = request.GET.get('sort', '')
        if sort:
            if sort == 'hot':
                all_teacher = all_teacher.order_by('-click_nums')
        # 教师排行
        hot_teachers = all_teacher.order_by('-click_nums')[:3]
        # 分页
        try:
            page = request.GET.get('page', 1)
        except PageNotAnInteger:
            page = 1
        p = Paginator(all_teacher, 5, request=request)
        teachers = p.page(page)
        current_nav = 'teacher'
        return render(request, 'teachers-list.html', {"all_teacher": teachers,
                                                      "teacher_count": teacher_count,
                                                      "sort": sort,
                                                      "hot_teachers": hot_teachers,
                                                      "current_nav": current_nav})


class TeacherDetailView(View):
    def get(self, request, teacher_id):
        teacher = Teacher.objects.get(id=int(teacher_id))
        teacher.click_nums += 1
        teacher.save()
        # 相关课程
        all_course = Course.objects.filter(teacher=teacher.id)
        # 教师排行
        all_teacher = Teacher.objects.all()
        hot_teachers = all_teacher.order_by('-click_nums')[:3]
        # 收藏
        has_fav1 = False
        has_fav2 = False
        if request.user.is_authenticated:
            if UserFavorate.objects.filter(user=request.user, fav_id=teacher.id, fav_type=3):
                has_fav1 = True
            if UserFavorate.objects.filter(user=request.user, fav_id=teacher.org_id, fav_type=2):
                has_fav2 = True
        return render(request, 'teacher-detail.html', {"teacher": teacher,
                                                       "hot_teachers": hot_teachers,
                                                       "all_course": all_course,
                                                       "has_fav1": has_fav1,
                                                       "has_fav2": has_fav2})
