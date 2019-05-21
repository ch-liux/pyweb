# _*_ encoding:utf-8 _*_

from django.shortcuts import render
from django.views.generic.base import View
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.backends import ModelBackend
from django.db.models import Q
from django.contrib.auth.hashers import make_password
from django.http import HttpResponseRedirect, HttpResponse
from django.urls import reverse

from .models import UserProfile, EmailVerifyRecord, Banner
from .forms import LoginForm, RegisterForm, ForgetForm, ModifyPwdForm, UploadImageForm, UserInfoForm
from apps.utils.send_email import send_register_email
from apps.utils.mixin_utils import LoginRequiredMixin
from apps.operation.models import UserCourse, Course, UserFavorate, UserMessage
from apps.organization.models import CourseOrg, Teacher

import json
from pure_pagination import Paginator, PageNotAnInteger
# Create your views here.


# 自定义auth验证
class CustomBackend(ModelBackend):
    def authenticate(self, request, username=None, password=None, **kwargs):
        try:
            # 验证用户，使用get验证只有一个
            # Q |并集 ,交集
            user = UserProfile.objects.get(Q(username=username) | Q(email=username))
            if user.check_password(password):
                return user
        except Exception as e:
            return None


class AciveUserView(View):
    def get(self, request, active_code):
        all_records = EmailVerifyRecord.objects.filter(code=active_code)
        if all_records:
            for record in all_records:
                email = record.email
                user = UserProfile.objects.get(email=email)
                user.is_active = True
                user.save()
        else:
            return render(request, "active_fail.html", {})
        return render(request, "login.html", {})


class RestView(View):
    def get(self, request, active_code):
        all_records = EmailVerifyRecord.objects.filter(code=active_code)
        if all_records:
            for record in all_records:
                email = record.email
                return render(request, "password_reset.html", {"email": email})
        else:
            return render(request, "active_fail.html", {})
        return render(request, "login.html", {})


class ModifyPwdView(View):
    def post(self, request):
        modify_form = ModifyPwdForm(request.POST)
        if modify_form.is_valid():
            pwd1 = request.POST.get("password1", "")
            pwd2 = request.POST.get("password2", "")
            email = request.POST.get("email", "")
            if pwd1 != pwd2:
                return render(request, "password_reset.html", {"email": email, "msg": "密码不一致"})
            user = UserProfile.objects.get(email=email)
            user.password = make_password(pwd2)
            user.save()

            return render(request, "login.html", {})
        else:
            email = request.POST.get("email", "")
            return render(request, "password_reset.html", {"email": email, "modify_form": modify_form})


class RegisterView(View):
    def get(self, request):
        register_form = RegisterForm()
        return render(request, 'register.html', {"register_form": register_form})

    def post(self, request):
        register_form = RegisterForm(request.POST)
        if register_form.is_valid():
            user_name = request.POST.get("email", "")
            if UserProfile.objects.filter(email=user_name):
                return render(request, "register.html", {"msg": "用户已存在", "register_form": register_form})
            pass_word = request.POST.get("password", "")
            user_profile = UserProfile()
            user_profile.username = user_name
            user_profile.email = user_name
            user_profile.is_active = False
            user_profile.password = make_password(pass_word) # 加密
            user_profile.save()

            user_message = UserMessage()
            user_message.user = user_profile.id
            user_message.message = '欢迎注册慕学网在线'
            user_message.save()

            send_register_email(user_name, "register")
            return render(request, "login.html", {})
        else:
            return render(request, "register.html", {"register_form": register_form})


class LogoutView(View):
    def get(self, request):
        logout(request)
        return HttpResponseRedirect(reverse('index'))


class LoginView(View):
    def get(self, request):
        return render(request, 'login.html', {})

    def post(self, request):
        login_form = LoginForm(request.POST)
        if login_form.is_valid():
            user_name = request.POST.get("username", "")
            pass_word = request.POST.get("password", "")
            user = authenticate(username=user_name, password=pass_word)
            if user is not None:
                if user.is_active:
                    login(request, user)
                    return HttpResponseRedirect(reverse('index'))
                    # return render(request, "index.html", {"user_name": user_name})
                else:
                    return render(request, "login.html", {"msg": "用户未激活"})
            else:
                return render(request, "login.html", {"msg": "用户名或密码错误"})
        else:
            return render(request, "login.html", {"login_form": login_form})


class ForgetPasswordView(View):
    def get(self, request):
        forget_form = ForgetForm()
        return render(request, "forgetpwd.html", {"forget_form": forget_form})

    def post(self, request):
        forget_form = ForgetForm(request.POST)
        if forget_form.is_valid():
            email = request.POST.get("email", "")
            send_register_email(email, "forget")
            return render(request, "send_success.html")
        else:
            return render(request, "forgetpwd.html", {"forget_form": forget_form})


class UserInfoView(LoginRequiredMixin, View):
    # 用户个人信息
    def get(self, request):
        return render(request, 'usercenter-info.html', {})

    def post(self, request):
        user_info_form = UserInfoForm(request.POST, instance=request.user)
        if user_info_form.is_valid():
            user_info_form.save()
            return HttpResponse('{"status":"success"}', content_type='application/json')
        else:
            return HttpResponse(json.dumps(user_info_form.errors), content_type='application/json')


class UserImageUpload(LoginRequiredMixin, View):
    # 修改头像
    def post(self, request):
        image_form = UploadImageForm(request.POST, request.FILES, instance=request.user)
        if image_form.is_valid():
            # image = image_form.cleaned_data['image']
            # request.user.image = image
            request.user.save()
            return HttpResponse('{"status":"success"}', content_type='application/json')
        else:
            return HttpResponse('{"status":"fail"}', content_type='application/json')


class UserModifyPwdView(View):
    def post(self, request):
        modify_form = ModifyPwdForm(request.POST)
        if modify_form.is_valid():
            pwd1 = request.POST.get("password1", "")
            pwd2 = request.POST.get("password2", "")
            if pwd1 != pwd2:
                return HttpResponse('{"status":"fail", "msg":"密码不一致"}', content_type='application/json')
            user = request.user
            user.password = make_password(pwd2)
            user.save()

            return HttpResponse('{"status":"success"}', content_type='application/json')
        else:
            return HttpResponse(json.dumps(modify_form.errors), content_type='application/json')


class SendEmailCodeView(LoginRequiredMixin, View):
    def get(self, request):
        email = request.GET.get("email", "")

        if UserProfile.objects.filter(email=email):
            return HttpResponse('{"email":"邮箱已存在"}', content_type='application/json')
        send_register_email(email, "update_email")
        return HttpResponse('{"status":"success"}', content_type='application/json')


class UpdateEmailView(LoginRequiredMixin, View):
    def post(self, request):
        email = request.POST.get("email", "")
        code = request.POST.get("email", "")

        existed_code = EmailVerifyRecord.objects.filter(email=email, code=code, send_type="update_email")
        if existed_code:
            user = request.user
            user.email = email
            user.save()
            return HttpResponse('{"status":"success"}', content_type='application/json')
        else:
            return HttpResponse('{"email":"验证码出错"}', content_type='application/json')


class MyCourseView(LoginRequiredMixin, View):
    def get(self, request):
        course_ids = UserCourse.objects.filter(user_id=request.user.id)
        courses = Course.objects.filter(id__in=course_ids)
        return render(request, 'usercenter-mycourse.html', {"courses": courses})


class MyFavOrgView(LoginRequiredMixin, View):
    def get(self, request):
        favorates = UserFavorate.objects.filter(user_id=request.user.id, fav_type=2)
        ord_ids = []
        for favorate in favorates:
            ord_ids.append(favorate.fav_id)
        orgs = CourseOrg.objects.filter(id__in=ord_ids)
        return render(request, 'usercenter-fav-org.html', {"orgs": orgs, "check": "org"})


class MyFavTeacherView(LoginRequiredMixin, View):
    def get(self, request):
        favorates = UserFavorate.objects.filter(user_id=request.user.id, fav_type=3)
        ord_ids = []
        for favorate in favorates:
            ord_ids.append(favorate.fav_id)
        teachers = Teacher.objects.filter(id__in=ord_ids)
        return render(request, 'usercenter-fav-teacher.html', {"teachers": teachers, "check": "teacher"})


class MyFavCourseView(LoginRequiredMixin, View):
    def get(self, request):
        favorates = UserFavorate.objects.filter(user_id=request.user.id, fav_type=1)
        ord_ids = []
        for favorate in favorates:
            ord_ids.append(favorate.fav_id)
        courses = Course.objects.filter(id__in=ord_ids)
        return render(request, 'usercenter-fav-course.html', {"courses": courses, "check": "course"})


class MyMeassageView(LoginRequiredMixin, View):
    def get(self, request):
        all_meassage = UserMessage.objects.filter(user=request.user.id)
        all_unread_msg = UserMessage.objects.filter(has_read=False, user=request.user.id)
        for unread in all_unread_msg:
            unread.has_read = True
            unread.save()
        try:
            page = request.GET.get('page', 1)
        except PageNotAnInteger:
            page = 1
        p = Paginator(all_meassage, 5, request=request)
        all_meassage = p.page(page)
        return render(request, 'usercenter-message.html', {"all_meassage": all_meassage})


class IndexView(View):
    def get(self, request):
        # 轮播图
        banners = Banner.objects.all().order_by('index')
        banner_courses = Course.objects.filter(is_banner=True)[:3]
        courses = Course.objects.filter(is_banner=False)[:6]
        orgs = CourseOrg.objects.all()[:15]
        return render(request, 'index.html', {"banners": banners,
                                              "banner_courses": banner_courses,
                                              "courses": courses,
                                              "orgs": orgs})


def page_not_found(request, **kwargs):
    from django.shortcuts import render_to_response
    response = render_to_response('404.html', {})
    response.status_code = 404
    return response


def page_error(request, **kwargs):
    from django.shortcuts import render_to_response
    response = render_to_response('500.html', {})
    response.status_code = 500
    return response
