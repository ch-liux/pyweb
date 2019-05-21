from django import forms
from captcha.fields import CaptchaField


# 注册验证
class LoginForm(forms.Form):
    username = forms.CharField(required=True, min_length=4, max_length=20)
    password = forms.CharField(required=True, min_length=6, max_length=16)
    captcha = CaptchaField(error_messages={"invalid": "验证码错误"})
