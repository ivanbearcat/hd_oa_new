# -*- coding: utf-8 -*-
from django.shortcuts import render
from django.http import HttpResponseRedirect
from django.utils.log import request_logger as logger
from django.contrib import auth



def login(request):
    return render(request, 'login/login.html')



def login_auth(request):
    user_auth = request.POST.get('username')
    passwd_auth = request.POST.get('password')
    authed = auth.authenticate(username=user_auth,password=passwd_auth)
    if authed and authed.is_active:
        auth.login(request,authed)

        next_page = request.session.get('next')
        if next_page:
            request.session.pop('next')
            return HttpResponseRedirect(next_page)
        else:
            return HttpResponseRedirect('/home/')
            # return render(request, 'login/login.html', {'code': 0, 'msg': '登陆成功'})
    else:
        logger.warn('<%s> login in fail.' % user_auth)
        return render(request, 'login/login.html', {'code': 1, 'msg': '账号或密码错误'})



def logout(request):
    auth.logout(request)
    return render(request, 'login/login.html')



def not_login(request):
    next_next = request.GET.get('next')
    request.session['next'] = next_next
    return render(request, 'login/login.html',{'msg': '您还没有登录'})

