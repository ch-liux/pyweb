from django.contrib import admin
from django.urls import path, include

from apps.user.views import IndexView



urlpatterns = [
    path('admin/', admin.site.urls),

    path('', IndexView.as_view()),  #TODO由nginx处理
    path('index/', IndexView.as_view(), name="index"),

    path('user/', include("apps.user.urls", namespace="user")),

    # 图片验证码
    path('captcha/', include('captcha.urls')),
]
