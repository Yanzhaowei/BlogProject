#!/usr/bin/env python
# -*- coding: utf8 -*-
#__Author: "Skiler Hao"
#date: 2017/3/30 15:40
from django.core.exceptions import ValidationError
from django import forms
from django.forms import fields
from django.forms import widgets
from django.core.validators import RegexValidator
from  .models import User



# 注册
class RegisterForm(forms.Form):
    '''
    注册表单
    '''
    name = forms.CharField(widget=forms.TextInput(attrs={"placeholder": "请输入用户名", "required": "required",}),
                          required=True, min_length=6,max_length=12,error_messages={"required": "用户名不能为空"}, label='用户名')
    Email = forms.EmailField(widget=forms.TextInput(attrs={"placeholder": "请输入邮箱", "required": "required",}),
                             required=True, max_length=50,error_messages={"required": "email不能为空",}, label='邮箱')
    mobile = forms.CharField(widget=forms.TextInput(attrs={"placeholder": "请输入手机号", }),
                              max_length=100, required=False, label='手机')
    pwd = forms.CharField(widget=forms.PasswordInput(attrs={"placeholder": "请输入密码", "required": "required",}),
                          required=True, max_length=20,error_messages={"required": "密码不能为空",}, label='密码')


# 登陆注册
class LoginForm(forms.Form):
    name = fields.CharField(
        required=True,
        widget=forms.TextInput(attrs={'class': "form-control",'placeholder': '请输入用户名'}),
        min_length=6,
        max_length=12,
        strip=True,
        error_messages={'required': '用户名不能为空',}
    )

    pwd = fields.CharField(
        widget=forms.PasswordInput(attrs={'class': "form-control",'placeholder': '请输入密码'}),
        required=True,
        min_length=6,
        max_length=12,
        strip=True,
        error_messages={'required': '密码不能为空!',}
    )

    def clean(self):
        username = self.cleaned_data.get('name')
        pwd = self.cleaned_data.get('pwd')
        user = User.objects.filter(name=username).first()
        if username and pwd:
            if not user :
                # self.error_dict['pwd_again'] = '两次密码不匹配'
                raise ValidationError('用户名不存在！')
            elif pwd != user.pwd:
                raise ValidationError('密码不正确！')

# 评论的forms
class CommentForm(forms.Form):
    content = forms.CharField(widget=forms.TextInput(),error_messages={"required": "评论不能为空"}, required=True)
    # article = forms.CharField(widget=forms.HiddenInput())

