from django.shortcuts import render
from django.http import JsonResponse
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
import json
from process.models import table as _table

@login_required
def table(request):
    return render(request, 'process/table.html',{'user': request.user.last_name,
                                                 'path1': 'process',
                                                 'path2': 'process_table',
                                                 'page_name1': '流程管理',
                                                 'page_name2': '流程表',})


@login_required
def table_data(request):
    orm = _table.objects.all()
    tableData = []
    for i in orm:
        tableData.append({
            'id': i.id,
            'name': i.name,
            'cities': i.cities,
            '_type': i._type,
            'description': i.description,
            'status': i.status,
            'processor': i.processor,
            'create_time': str(i.create_time).split('.')[0],
        })
    return JsonResponse({'code': -1, 'tableData': tableData})


@login_required
def table_save(request):
    data = json.loads(request.body)
    name = request.user.last_name
    cities = data.get('cities')
    _type = data.get('_type')
    description = data.get('description')
    orm = _table(name=name, cities=cities, _type=_type, description=description)
    orm.save()
    return JsonResponse({'code': 0, 'msg': '操作成功'})


@login_required
def table_commit(request):
    data = json.loads(request.body)
    id = data.get('id')
    orm = _table.objects.get(id=id)
    orm.status = '已完成'
    orm.processor = request.user.last_name
    orm.save()
    return JsonResponse({'code': 0, 'msg': '操作成功'})


@login_required
def table_del(request):
    data = json.loads(request.body)
    id = data.get('id')
    orm = _table.objects.get(id=id)
    orm.delete()
    return JsonResponse({'code': 0, 'msg': '撤销成功'})