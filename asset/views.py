#coding:utf-8
from django.shortcuts import render
from django.http import HttpResponse
from django.contrib.auth.decorators import login_required
import json
from asset.models import table as _table
from libs.ldap_pack import search_user_info


@login_required
def table(request):
    username = search_user_info(request.user.username).get('name')
    return render(request, 'asset/table.html',{'user': username,
                                               'path1': 'asset',
                                               'path2': 'asset_table',
                                               'page_name1': '资产管理',
                                               'page_name2': '资产表',})



@login_required
def table_data(request):
    username = search_user_info(request.user.username).get('name')
    orm = _table.objects.filter(owner=username)
    tableData = []
    for i in orm:
        tableData.append({
            'id': i.id,
            'name': i.name,
            '_type': i._type,
            'sn_mainboard': i.sn_mainboard,
            'sn_BIOS': i.sn_BIOS,
            'organization': i.organization,
            'location': i.location,
            'new_asset_number': i.new_asset_number,
            'owner': i.owner,
            'owner_department': i.owner_department,
            'is_use': i.is_use,
            'cost_center': i.cost_center,
            'checker': i.checker,
            'create_time': str(i.create_time).split('+')[0],
        })
    return HttpResponse(json.dumps({'code': -1, 'tableData': tableData}), content_type="application/json")



@login_required
def table_approve(request):
    # data = json.loads(request.body)
    # print(data.get('id'))
    id = request.GET.get('id')
    print(id)

    return HttpResponse(json.dumps({'code': -1, 'tableData': 1}), content_type="application/json")