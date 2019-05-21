from django.shortcuts import render
from django.views.generic.base import View
from django.contrib.auth import authenticate, login, logout
from django.http import HttpResponseRedirect, HttpResponse, QueryDict
from django.urls import reverse
from django.contrib.auth.hashers import make_password, check_password

from .forms import LoginForm
from .models import UserProfile
from utils.tools import CaptchaUtil, ResultView
from utils.mixin import LoginRequiredMixin

import json
from datetime import datetime
from pure_pagination import Paginator, PageNotAnInteger


class LoginView(View):

    def get(self, request):
        context = CaptchaUtil().captcha()
        return render(request, 'login.html', context)
    
    def post(self, request):
        login_form = LoginForm(request.POST)
        if login_form.is_valid():
            username = request.POST.get('username')
            password = request.POST.get('password')
            user = authenticate(username=username, password=password)
            if user:
                login(request, user)
                # 是否跳转
                next_url = request.GET.get('next', reverse("index"))
                response = HttpResponseRedirect(next_url)
                return response
            context = CaptchaUtil().captcha()
            context['login_form'] = {
                "errors":{"username":"username","password":"password"},
                "password":{"value":password},
                "username":{"value":username}
            }
            return render(request, 'login.html', context)
        else:
            context = CaptchaUtil().captcha()
            context['login_form'] = login_form
            return render(request, "login.html", context)


class LogoutView(LoginRequiredMixin, View):

    def get(self, request):
        logout(request)
        return HttpResponseRedirect(reverse("user:login"))


class IndexView(LoginRequiredMixin, View):
     
    def get(self, request):
        return render(request, 'index.html', {})


class IndexContentView(LoginRequiredMixin, View):

    def get(self, request):
        us = UserProfile.objects.all().count()
        context = {"us":us}
        return render(request, 'index_content.html', context)


class UserView(LoginRequiredMixin, ResultView, View):

    def get(self, request):
        return render(request, 'user/user.html', {})
    
    def post(self, request):
        # d = request._post.dict()
        uid = request.POST.get('id')
        nickname = request.POST.get('nickname')
        gender = request.POST.get('gender')
        birthday = request.POST.get('birthday')
        email = request.POST.get('email')
        mobile = request.POST.get('mobile')
        address = request.POST.get('address')
        desc = request.POST.get('desc')
        if not all([uid, nickname, gender, birthday, email, mobile, address]):
            self.r['msg'] = "获取数据失败."
            self.r['code'] = 1
            return HttpResponse(json.dumps(self.r), content_type='application/json')
        try:
            user = UserProfile.objects.get(pk=uid)
        except Exception as e:
            self.r['msg'] = "用户不存在."
            self.r['code'] = 2
            self.r['exec'] = str(e.args)
            return HttpResponse(json.dumps(self.r), content_type='application/json')
        
        if gender not in ("male","female"):
            self.r['msg'] = "性别不详."
            self.r['code'] = 3
            return HttpResponse(json.dumps(self.r), content_type='application/json')

        birthday = datetime.strptime(birthday, "%Y年%m月%d日")
        user.nickname = nickname
        user.gender = gender
        user.birthday = birthday
        user.email = email
        user.mobile = mobile
        user.desc = desc
        user.address = address

        user.save()
        self.r['msg'] = "修改成功."
        return HttpResponse(json.dumps(self.r), content_type='application/json')

    def put(self, request):
        qd = QueryDict(request.body)
        pd = {k: v[0] if len(v)==1 else v for k, v in qd.lists()}
        uid = pd.get('id')
        pwd1 = pd.get('pwd1')
        pwd2 = pd.get('pwd2')
        pwd3 = pd.get('pwd3')

        if pwd2 != pwd3:
            self.r['msg'] = "密码不一致."
            self.r['code'] = 1
            return HttpResponse(json.dumps(self.r), content_type='application/json')

        try:
            user = UserProfile.objects.get(pk=uid)
        except Exception as e:
            self.r['msg'] = "用户不存在."
            self.r['code'] = 2
            self.r['exec'] = str(e.args)
            return HttpResponse(json.dumps(self.r), content_type='application/json')

        if not check_password(pwd1, user.password):
            self.r['msg'] = "旧密码错误."
            self.r['code'] = 3
            return HttpResponse(json.dumps(self.r), content_type='application/json')
        
        user.password = make_password(pwd2, None, 'pbkdf2_sha256')

        user.save()
        self.r['msg'] = "修改成功."
        return HttpResponse(json.dumps(self.r), content_type='application/json')


class AccountView(LoginRequiredMixin, ResultView, View):

    def get(self, request):
        return render(request, 'user/account.html', {})


class DataView(LoginRequiredMixin, ResultView, View):

    def get(self, request):
        page = request.GET.get('page', 1)
        limit = request.GET.get('limit', 10)
        skey = request.GET.get('skey', '')
        gender = request.GET.get('gender', '')
        data = []
        try:
            page = int(page)
            limit = int(limit)

            users = UserProfile.objects.filter(username__contains=skey)
            if gender:
                users = users.filter(gender=gender)
            pobj = Paginator(users, limit, request=request)
            datas = pobj.page(page)

            for u in datas.object_list:
                data.append({
                    "id":u.id, "username":u.username, "desc":u.desc, "addDate":self.dt_to_str(u.date_joined), 
                    "birthday":self.dt_to_str(u.birthday), "email":u.email, "mobile":u.mobile, "address":u.address,
                    "nickname":u.nickname, "gender":u.gender
                })

            self.r['count'] = len(users)
            self.r['data'] = data
            return HttpResponse(json.dumps(self.r), content_type='application/json')
        except Exception as e:
            self.r['msg'] = '查询异常'
            self.r['code'] = '1'
            self.r['exec'] = str(e.args)
            return HttpResponse(json.dumps(self.r), content_type='application/json')
    
    def dt_to_str(self, dt):
        return dt.strftime("%Y-%m-%d")
