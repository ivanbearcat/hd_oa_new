#coding:utf-8
from django.shortcuts import render
from django.http import HttpResponse
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
import json
from django.contrib import auth
from libs.ldap_pack import search_user_info, change_passwd


@login_required
def chpasswd(request):
    return render(request, 'user/chpasswd.html',{'user': request.user.username,
                                                 'path1': 'user_manage',
                                                 'path2': 'chpasswd',
                                                 'page_name1': '用户管理',
                                                 'page_name2': '修改密码',})

@login_required
def post_chpasswd(request):
    password_current = request.POST.get('password_current')
    password_new = request.POST.get('password_new')
    password_new_again = request.POST.get('password_new_again')
    user = User.objects.get(username=request.user.username)
    if not user.check_password(password_current):
        code = 1
        msg = u'当前密码错误'
    elif password_new == '' or password_new_again == '':
        code = 2
        msg = u'新密码不能为空'
    elif not password_new == password_new_again:
        code = 3
        msg = u'新密码不一致'
    else:
        try:
            user.set_password(password_new)
            user.save()
            code = 0
            msg = u'密码修改成功'
        except Exception:
            code = 4
            msg = u'密码修改失败'
    return HttpResponse(json.dumps({'code':code,'msg':msg}),content_type="application/json")


@login_required
def post_chpasswd_ldap(request):
    password_current = request.POST.get('password_current')
    password_new = request.POST.get('password_new')
    password_new_again = request.POST.get('password_new_again')
    username = request.user.username

    authed = auth.authenticate(username=username, password=password_current)
    if not authed:
        code = 1
        msg = u'当前密码错误或账号不可用'
    elif password_new == '' or password_new_again == '':
        code = 2
        msg = u'新密码不能为空'
    elif not password_new == password_new_again:
        code = 3
        msg = u'新密码不一致'
    else:
        result = change_passwd(username, password_new)
        if result:
            code = 0
            msg = u'密码修改成功'
        else:
            code = 4
            msg = u'密码修改失败（请检查密码复杂度）'
    return HttpResponse(json.dumps({'code':code,'msg':msg}),content_type="application/json")




