"""hd_oa URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, include
from django.conf.urls import url
from login.views import *
from home.views import home


admin.site.site_header = "航动资产管理"
admin.site.site_title = "航动资产管理"
admin.site.index_title = "资产管理"


urlpatterns = [
    path('admin/', admin.site.urls),
    url(r'^$', login),
    url(r'^login_auth/$', login_auth),
    url(r'^logout/$', logout),
    url(r'^accounts/login/$', not_login),
    url(r'^home/$', home),
    path('user/', include('user.urls')),
    path('asset/', include('asset.urls')),
]
