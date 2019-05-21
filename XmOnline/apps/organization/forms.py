# _*_ encoding:utf-8 _*_
from django import forms
from apps.operation.models import UserAsk

import re

# 自定义form
# class UserAskForm(forms.Form):
#     name = forms.CharField(required=True, min_length=2, max_length=20)
#     mobile = forms.CharField(required=True, min_length=11, max_length=11)
#     course_name = forms.CharField(required=True, min_length=5, max_length=5)


# model-form
class UserAskForm(forms.ModelForm):
    # my_field = forms.CharField() # 新增自定义字段
    class Meta:
        model = UserAsk
        fields = ['name', 'mobile', 'course_name']

    def clean_mobile(self):
        mobile = self.cleaned_data['mobile']
        p = re.compile("^[1][3,4,5,7,8][0-9]{9}$")
        if p.match(mobile):
            return mobile
        else:
            raise forms.ValidationError("手机号码非法", code="mobile_invalid")
