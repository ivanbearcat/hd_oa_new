from django.shortcuts import render
from django.template import RequestContext
from django.contrib.auth.decorators import login_required

@login_required
def home(request):
    return render(request,'public/index.html',{'user': request.user.username,
                                               'path1': 'home',
                                               'page_name1': '主页'})
